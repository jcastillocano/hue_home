from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from lights.settings import HUE_HOST, HUE_TOKEN
from hueber.api import Bridge
from hueber.lib import LightBuilder
from .models import Light
import json


def _lightdict(light):
    on = "On" if light.data["state"]["on"] else "Off"
    reachable = "Online" if light.data["state"]["reachable"] else "Offline"
    return {
        "Name": light["name"],
        "on": on,
        "reachable": reachable,
        "type": light["type"],
    }


def _on(on_off):
    return on_off == "On"


# Create your views here.
def sync(request):
    hue = Bridge(HUE_HOST, HUE_TOKEN)
    light_map = {k: _lightdict(v) for k, v in hue.lights.items()}
    for _id, values in light_map.items():
        try:
            obj = Light.objects.get(light_id=int(_id))
            print("Object found: %s" % obj)
            obj.name = values["Name"]
            obj.on = _on(values["on"])
            obj.reachable = values["reachable"]
            obj.type = values["type"]
            obj.value = int(100 * int(hue.lights[_id].data["state"]["bri"]) / 255)
        except Light.DoesNotExist:
            print("Creating new object")
            obj = Light.objects.create(
                light_id=int(_id),
                name=values["Name"],
                on=_on(values["on"]),
                reachable=values["reachable"],
                type=values["type"],
                value=int(100 * int(hue.lights[_id].data["state"]["bri"]) / 254),
            )
        obj.save()

    context = {
        "lights": Light.objects.all(),
        "switchoff": Light.objects.filter(on=True).count(),
    }
    return render(request, "hue/index.html", context)


def update(request, light_id):
    post = request.POST
    value = int(post["value"])
    if value < 1:
        value = 1
    if value > 100:
        value = 100

    hue = Bridge(HUE_HOST, HUE_TOKEN)
    update = LightBuilder()
    update["on"] = "on" in post
    update["bri"] = int(254 * int(value) / 100) + 1
    print("Updating light %s with values %s" % (light_id, update.update_str()))
    hue.lights[light_id].push(update.update_str())
    print(hue.lights[light_id])
    print("Light %s updated" % light_id)
    return HttpResponseRedirect(reverse("list", args=()))


def shutdown(request):
    hue = Bridge(HUE_HOST, HUE_TOKEN)
    for light in Light.objects.filter(on=True):
        update = LightBuilder()
        update["on"] = False
        print("Switching off %s light" % light.light_id)
        hue.lights[light.light_id].push(update.update_str())
    return HttpResponseRedirect(reverse("list", args=()))
