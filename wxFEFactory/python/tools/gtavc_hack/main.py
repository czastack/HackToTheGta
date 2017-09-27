from lib.hack.form import Group, InputWidget, CheckBoxWidget, CoordWidget, ModelInputWidget, ModelCoordWidget
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.win32.sendkey import auto, TextVK
from commonstyle import dialog_style, styles
from . import address, models
from .models import Player, Vehicle
from .data import SLOT_NO_AMMO, WEAPON_LIST, VEHICLE_LIST
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
    SPHERE_RANGE = 16

    FUNCTION_REQUEST_MODEL = b'\x55\x8B\xEC\x51\xC7\x45\xFC\x10\xE3\x40\x00\x6A\x16\xFF\x75\x08\xFF\x55\xFC\x83\xC4\x08\x8B\xE5\x5D\xC3'
    FUNCTION_LOAD_REQUESTED_MODELS = b'\x55\x8B\xEC\x51\xC7\x45\xFC\xF0\xB5\x40\x00\x6A\x00\xFF\x55\xFC\x83\xC4\x04\x8B\xE5\x5D\xC3'

    jetPackSpeed = 2.0

    def render(self):
        with self.render_win() as win:
            with ui.Vertical():
                with ui.Horizontal(className="expand container"):
                    ui.Button("检测", className="vcenter", onclick=self.checkAttach)
                    self.attach_status_view = ui.Text("", className="label_left grow")
                    ui.CheckBox("保持最前", onchange=self.swithKeeptop)
                with ui.Notebook(className="fill"):
                    self.render_main()

        win.setOnClose(self.onClose)

    def render_main(self):
        with Group("player", "角色", self._player, handler=self.handler):
            self.hp_view = ModelInputWidget("hp", "生命")
            self.ap_view = ModelInputWidget("ap", "防弹衣")
            self.rot_view = ModelInputWidget("rotation", "旋转")
            self.coord_view = ModelCoordWidget("coord", "坐标", savable=True)
            self.speed_view = ModelCoordWidget("speed", "速度")
            self.weight_view = ModelInputWidget("weight", "重量")
            self.stamina_view = ModelInputWidget("stamina", "体力")
            self.wanted_view = ModelInputWidget("wanted_level", "通缉等级")
            ui.Text("")
            ui.Button(label="车坐标->人坐标", onclick=self.from_vehicle_coord)
        with Group("vehicle", "汽车", self._vehicle, handler=self.handler):
            self.vehicle_hp_view = ModelInputWidget("hp", "HP")
            self.vehicle_roll_view = ModelCoordWidget("roll", "滚动")
            self.vehicle_dir_view = ModelCoordWidget("dir", "方向")
            self.vehicle_coord_view = ModelCoordWidget("coord", "坐标", savable=True)
            self.vehicle_speed_view = ModelCoordWidget("speed", "速度")
            self.vehicle_turn_view = ModelCoordWidget("turn", "Turn")
            self.weight_view = ModelInputWidget("weight", "重量")
            ui.Text("")
            ui.Button(label="人坐标->车坐标", onclick=self.from_player_coord)

        with Group("weapon", "武器槽", None, handler=self.handler):
            self.weapon_views = []
            for i in range(11):
                self.weapon_views.append(
                    WeaponWidget("weapon%d" % i, "武器槽%d" % i, i, SLOT_NO_AMMO, WEAPON_LIST, self._player, self.on_weapon_change)
                )

        with Group("global", "全局", 0, handler=self.handler):
            self.money_view = InputWidget("money", "金钱", address.MONEY, (), int)
            self.camera_view = CoordWidget("camera", "摄像机", 0x7E46B8, ())
            self.camera_z_rot_view = InputWidget("camera_z_rot", "摄像机z_rot", 0x7E48CC, (), float)
            self.camera_x_rot_view = InputWidget("camera_x_rot", "摄像机x_rot", 0x7E48BC, (), float)

        with Group(None, "作弊", 0, handler=self.handler, flexgrid=False, hasfootbar=False):
            with ui.Vertical(className="fill container"):
                with ui.GridLayout(cols=4, vgap=10, className="fill container"):
                    CheckBoxWidget("god1", "角色无伤1", 0x5267DC, (), b'\xEB\x10', b'\x75\x15')
                    CheckBoxWidget("god2", "角色无伤2", 0x5267D5, (), b'\x90\x90', b'\x75\x1C')
                    CheckBoxWidget("vehicle_god1", "汽车无伤1", 0x5A9801, (), b'\xc7\x41\x04\x00\x00\x00\x00\xc2\x04', b'\x88\x41\x04\xc2\x04\x00\x00\x00\x00')
                    CheckBoxWidget("vehicle_god2", "汽车无伤2", 0x588A77, (), b'\x90\x90', b'\x75\x09')
                    CheckBoxWidget("infinite_run", "无限奔跑", 0x536F25, (), b'\xEB', b'\x75')
                    CheckBoxWidget("drive_on_water", "水上开车", 0x593908, (), b'\x90\x90', b'\x74\x07')
                    CheckBoxWidget("no_falling_off_the_bike", "摩托老司机", 0x61393D, (), b'\xE9\xBC\x0E\x00\x00\x90', b'\x0F\x84\xBB\x0E\x00\x90')
                    CheckBoxWidget("disable_vehicle_explosions", "不会爆炸", 0x588A77, (), b'\x90\x90', b'\x75\x09')
                    CheckBoxWidget("infinite_ammo1", "无限子弹1", 0x5D4ABE, (), b'\x90\x90\x90', b'\xFF\x4E\x08')
                    CheckBoxWidget("infinite_ammo2", "无限子弹2", 0x5D4AF5, (), b'\x90\x90\x90', b'\xFF\x4E\x0C')

        with Group(None, "快捷键", 0, handler=self.handler, flexgrid=False, hasfootbar=False):
            with ui.Horizontal(className="fill container"):
                self.spawn_vehicle_id_view = ui.ListBox(className="expand", onselect=self.onSpawnVehicleIdChange, 
                    choices=(item[0] for item in VEHICLE_LIST))
                with ui.ScrollView(className="fill container"):
                    self.render_common_text()
                    ui.Text("根据左边列表生产载具: alt+V")
                    ui.Text("切换上一辆: alt+[")
                    ui.Text("切换下一辆: alt+]")
                    ui.Text("附近车辆爆炸(使用秘籍BIGBANG): alt+enter")
        with Group(None, "测试", 0, handler=self.handler, flexgrid=False, hasfootbar=False):
            with ui.GridLayout(cols=3, vgap=10, className="fill container"):
                ui.Button("杀掉附近的人", onclick=self.kill_near_persons)
                ui.Button("附近的车起火", onclick=self.near_vehicles_boom)
                ui.Button("附近的车下陷", onclick=self.near_vehicles_down)
                ui.Button("附近的车移到眼前", onclick=self.near_vehicles_to_front)
                ui.Button("附近的人移到眼前", onclick=self.near_persons_to_front)
                ui.Button("附近的车上天", onclick=self.near_vehicles_fly)
                ui.Button("附近的人上天", onclick=self.near_persons_fly)
                ui.Button("附近的车翻转", onclick=self.near_vehicles_flip)
                ui.Button("跳上一辆车", onclick=self.jump_on_vehicle)
                ui.Button("召唤上一辆车回来", onclick=self.call_vehicle)
                ui.Button("回到上一辆车旁边", onclick=self.go_vehicle)
        with Group(None, "工具", 0, flexgrid=False, hasfootbar=False):
            with ui.Vertical(className="fill container"):
                ui.Button("g3l坐标转json", onclick=self.g3l2json)

    def onClose(self, _=None):
        self.free_remote_function()

    def init_remote_function(self):
        self.RequestModel = self.handler.write_function(self.FUNCTION_REQUEST_MODEL)
        self.LoadRequestedModels = self.handler.write_function(self.FUNCTION_LOAD_REQUESTED_MODELS)

    def free_remote_function(self):
        self.handler.free_memory(self.RequestModel)
        self.handler.free_memory(self.LoadRequestedModels)

    def checkAttach(self, _=None):
        className = 'Grand theft auto 3'
        windowName = 'GTA: Vice City'

        if self.handler.active:
            self.free_remote_function()

        if self.handler.attachByWindowName(className, windowName):
            self.attach_status_view.label = windowName + ' 正在运行'

            if not self.win.hotkeys:
                self.win.RegisterHotKeys(
                    (
                        ('bigbang', MOD_ALT, getVK('enter'), self.bigbang),
                        ('spawnVehicle', MOD_ALT, getVK('v'), self.spawnVehicle),
                        ('spawnVehicleIdPrev', MOD_ALT, getVK('['), self.onSpawnVehicleIdPrev),
                        ('spawnVehicleIdNext', MOD_ALT, getVK(']'), self.onSpawnVehicleIdNext),
                        ('re_cal_spheres', MOD_ALT, getVK(";"), self.re_cal_spheres),
                        ('go_next_sphere', MOD_ALT | MOD_SHIFT, getVK(';'), self.go_next_sphere),
                    ) + self.get_common_hotkeys()
                )
            self.init_remote_function()
        else:
            self.attach_status_view.label = '没有检测到 ' + windowName

    def is_model_loaded(self, model_id):
        return self.handler.read8(address.MODEL_INFO + 20 * model_id) == 1

    def load_model(self, model_id):
        if model_id > 0 and not self.is_model_loaded(model_id):
            self.handler.remote_call(self.RequestModel, model_id)
            self.handler.remote_call(self.LoadRequestedModels, 0)

    def on_weapon_change(self, weapon_view):
        self.load_model(weapon_view.selected_item[1])

    def get_rotz(self):
        if self.isInVehicle:
            rotz = self.camera_z_rot_view.mem_value
        else:
            PI = math.pi
            HALF_PI = PI / 2
            rotz = self.rot_view.mem_value
            rotz += HALF_PI
            if rotz > PI:
                rotz += PI * 2
        return rotz

    def promptWrite(self, text):
        text = (text + '\0').encode('utf-16le')
        TEXT1_ADDR = 0x7D3E40
        TEXT2_ADDR = 0x939028
        
        self.handler.ptrsWrite(TEXT1_ADDR, (), text)
        time.sleep(0.01)
        self.handler.ptrsWrite(TEXT2_ADDR, (), text)

    def bigbang(self, _=None):
        self.inputCheat('bigbang')

    def spawnVehicle(self, _=None):
        self.inputCheat('betterthanwalking')

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

    def re_cal_spheres(self, _=None):
        """重新获取人/车标记点"""
        addr = self.address.SPHERE_ARRAY
        it = self.models.Sphere(addr, self.handler)
        self._spheres = []

        for i in range(self.SPHERE_RANGE):
            if it.coord[0]:
                self._spheres.append(it.clone())
            it.next()

        self._sphere_index = 0

    def go_next_sphere(self, _=None):
        """到下一处 人/车标记点"""
        if not hasattr(self, '_spheres'):
            self.re_cal_spheres()

        while True:
            try:
                item = self._spheres[self._sphere_index]
            except IndexError:
                self.re_cal_spheres()
                return
            if item.coord[0]:
                self.entity.coord = item.coord
                break
            self._sphere_index += 1