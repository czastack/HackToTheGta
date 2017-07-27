import fefactory_api
from commonstyle import styles

ui = fefactory_api.layout

class ListDialog(ui.StdModalDialog):
    def __init__(self, *args, listbox={}, **kwargs):
        super().__init__(*args, **kwargs)

        with self:
            with ui.Vertical(styles=styles, style=styles['class']['fill']):
                self.listbox = ui.CheckListBox(className='fill', **listbox)
                with ui.Horizontal(className="expand"):
                    ui.Button(label="全选", className="button", onclick=self.checkAll)
                    ui.Button(label="反选", className="button", onclick=self.reverseCheck)

    def checkAll(self, btn):
        self.listbox.checkAll()

    def reverseCheck(self, btn):
        self.listbox.reverseCheck()


class ChoiceDialog(ui.StdModalDialog):
    def __init__(self, *args, combobox={}, **kwargs):
        super().__init__(*args, **kwargs)

        with self:
            with ui.Vertical(styles=styles, style=styles['class']['fill']):
                self.combobox = ui.ComboBox(type="simple", className='fill', **combobox)

