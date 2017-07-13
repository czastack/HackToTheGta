from modules import modules
import fefactory_api
import fefactory
import traceback
import imp

ui = fefactory_api.layout

if __name__ == 'mainframe':
    winstyle = {
        'width': 1200,
        'height': 960,
    }

    styles = {
        'type': {

        },
        'class': {
            
        }
    }

    consoleStyle = {
        'height': 300,
    }
    consoleInputStyle = {
        'expand': True,
        'showPadding': '1 0 0 0',
    }
    consoleOutputStyle = {
        'expand': True,
        'flex': 1,
    }

    def onNav(name, index):
        try:
            module = getattr(__import__('modules.' + name), name) # , fromlist=['main']
            module.run()
        except Exception as e:
            print('加载模块%s失败' % name)
            traceback.print_exc()

    def closeWindow(m=None):
        win.close()

    def restart(m):
        closeWindow()
        fefactory.reload()
        import mainframe
        imp.reload(mainframe)

    with ui.MenuBar() as m:
        with ui.Menu("文件"):
            ui.MenuItem("打开\tCtrl+O")
            ui.MenuItem("重启\tCtrl+R", onselect=restart)
            ui.MenuItem("关闭")
        with ui.Menu("窗口"):
            ui.MenuItem("关闭\tCtrl+W", onselect=closeWindow)

    with ui.Window("火纹工厂", style=winstyle, styles=styles, menuBar=m) as win:
        with ui.AuiManager():
            ui.AuiItem(ui.ListBox(options=modules, values=lambda x: x, onselect=onNav))
            ui.AuiItem(ui.AuiNotebook(key="book"), direction="center", maximizeButton=True)
            with ui.Vertical(style=consoleStyle) as console:
                consol_output = ui.TextInput(readonly=True, multiline=True, style=consoleOutputStyle)
                consol_input = ui.TextInput(extStyle=0x0400, style=consoleInputStyle)
            ui.AuiItem(console, direction="bottom", caption="控制台", maximizeButton=True)

    def onselect(*args):
        print(args)

    with ui.ContextMenu(onselect=onselect) as cm:
        ui.MenuItem("测试")
    win.book.setContextMenu(cm)
    fefactory_api.setConsoleElem(consol_input, consol_output)
