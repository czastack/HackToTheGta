from functools import partial
from lib.hack.form import Group, InputWidget, CheckBoxWidget, CoordWidget, ModelInputWidget, ModelCoordWidget
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.win32.sendkey import auto, TextVK
from commonstyle import dialog_style, styles
from . import address, models
from .data import SLOT_NO_AMMO, WEAPON_LIST, VEHICLE_LIST
from .models import Player, Vehicle
from ..gta_base.main import BaseGTATool
from ..gta_base.widgets import WeaponWidget
import math
import os
import json
import time
import __main__
import fefactory_api
ui = fefactory_api.ui


class Tool(BaseGTATool):
    address = address
    models = models
    Player = Player
    Vehicle = Vehicle
    MARKER_RANGE = 32

    SAFE_SPEED_RATE = 0.3
    GO_FORWARD_COORD_RATE = 2.0

    def render_main(self):
        with Group("player", "角色", self._player, handler=self.handler):
            self.hp_view = ModelInputWidget("hp", "生命")
            self.ap_view = ModelInputWidget("ap", "防弹衣")
            self.rot_view = ModelInputWidget("rotation", "旋转")
            self.coord_view = ModelCoordWidget("coord", "坐标", savable=True)
            self.speed_view = ModelCoordWidget("speed", "速度")
            self.weight_view = ModelInputWidget("weight", "重量")
            # self.stamina_view = InputWidget("stamina", "体力", None, (0x600,), float)
            self.star_view = InputWidget("star", "通缉等级", address.WANTED_BASE, (0x53c, 0x18), int)
            ui.Text("")
            ui.Button(label="车坐标->人坐标", onclick=self.from_vehicle_coord)
        with Group("vehicle", "汽车", self._vehicle, handler=self.handler):
            self.vehicle_hp_view = ModelInputWidget("hp", "HP")
            self.vehicle_roll_view = ModelCoordWidget("roll", "滚动")
            self.vehicle_dir_view = ModelCoordWidget("dir", "方向")
            self.vehicle_coord_view = ModelCoordWidget("coord", "坐标", savable=True)
            self.vehicle_speed_view = ModelCoordWidget("speed", "速度")
            self.weight_view = ModelInputWidget("weight", "重量")
            ui.Text("")
            with ui.Horizontal(className="expand"):
                ui.Button(label="人坐标->车坐标", onclick=self.from_player_coord)
                ui.Button(label="锁车", onclick=self.vehicle_lock_door)
                ui.Button(label="开锁", onclick=partial(self.vehicle_lock_door, lock=False))

        with Group("weapon", "武器槽", None, handler=self.handler):
            self.weapon_views = []
            for i in range(1, 13):
                self.weapon_views.append(WeaponWidget("weapon%d" % i, "武器槽%d" % i, i, SLOT_NO_AMMO, WEAPON_LIST, self._player))

            ui.Button(label="一键最大", onclick=self.weapon_max)

        with Group("global", "全局", 0, handler=self.handler):
            self.money_view = InputWidget("money", "金钱", address.MONEY, (), int)
            
        with Group(None, "快捷键", 0, handler=self.handler, flexgrid=False, hasfootbar=False):
            with ui.Horizontal(className="fill container"):
                self.spawn_vehicle_id_view = ui.ListBox(className="expand", onselect=self.onSpawnVehicleIdChange, 
                    choices=(item[0] for item in VEHICLE_LIST))
                with ui.ScrollView(className="fill container"):
                    self.render_common_text()
        with Group(None, "测试", 0, handler=self.handler, flexgrid=False, hasfootbar=False):
            with ui.GridLayout(cols=3, vgap=10, className="fill container"):
                self.render_common_button()

        with Group(None, "工具", 0, flexgrid=False, hasfootbar=False):
            with ui.Vertical(className="fill container"):
                ui.Button("g3l坐标转json", onclick=self.g3l2json)

    def checkAttach(self, _=None):
        className = 'Grand theft auto 3'
        windowName = 'GTA3'
        if self.handler.attachByWindowName(className, windowName):
            self.attach_status_view.label = windowName + ' 正在运行'

            if not self.win.hotkeys:
                self.win.RegisterHotKeys(
                    self.get_common_hotkeys()
                )
        else:
            self.attach_status_view.label = '没有检测到 ' + windowName

    def onSpawnVehicleIdChange(self, lb):
        self.handler.write32(address.SPAWN_VEHICLE_ID_BASE, VEHICLE_LIST[lb.index][1])

    def onSpawnVehicleIdPrev(self, _=None):
        pos = self.spawn_vehicle_id_view.index
        if pos == 0:
            pos = len(VEHICLE_LIST)
        self.spawn_vehicle_id_view.setSelection(pos - 1, True)

    def onSpawnVehicleIdNext(self, _=None):
        pos = self.spawn_vehicle_id_view.index
        if pos == len(VEHICLE_LIST) - 1:
            pos = -1
        self.spawn_vehicle_id_view.setSelection(pos + 1, True)

    def vehicle_lock_door(self, _=None, lock=True):
        car = self.player.vehicle
        if car:
            if lock:
                car.lock_door()
            else:
                car.unlock_door()

    def weapon_max(self, _=None):
        for v in self.weapon_views:
            v.id_view.index = 1
            if v.has_ammo:
                v.ammo_view.value = 9999