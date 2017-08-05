#include <wx/wx.h>
#include "datacontrols.h"

void PropertyGrid::OnChange(wxPropertyGridEvent & event)
{
	m_changed = true;
	if (m_autosave)
	{
		auto p = event.GetProperty();
		pycref name = py::cast(p->GetName());
		pycref value = getValue(event.GetValue());
		if (m_onchange != None)
		{
			pycref ret = pyCall(m_onchange, this, name, value);
			if (ret.ptr() == Py_False)
			{
				// 返回False忽略当前改动
				event.Veto();
				return;
			}
			else if (ret.ptr() != Py_True)
			{
				event.Skip();
			}
		}
		m_data[name] = value;
	}
	else {
		event.Skip();
	}
}

void PropertyGrid::addFlagsProperty(wxcstr title, wxcstr name, pycref help, pycref py_items, pycref py_values, int value) {
	wxArrayString labels;
	wxArrayInt values;
	addAll(labels, py_items);
	if (!py_values.is_none())
	{
		addAll(values, py::iterable(py_values));
	}
	else
	{
		for (uint i = 0; i < labels.size(); ++i)
		{
			values.Add(1 << i);
		}
	}
	wxPGProperty* property = new wxFlagsProperty(title, name, labels, values, value);
	property->SetAttribute(wxPG_BOOL_USE_CHECKBOX, true);
	Append(property, help);
}

pyobj PropertyGrid::getValue(const wxVariant & value) {
	wxcstr type = value.GetType();
	if (type == "long")
		return py::cast(value.GetLong());
	else if (type == "string")
		return py::cast(value.GetString());
	else if (type == "bool")
		return py::cast(value.GetBool());
	else if (type == "arrstring") {
		const wxArrayString &&list = value.GetArrayString();
		py::list pylist(list.size());
		int i = 0;
		for (auto &e : list)
		{
			pylist[i++] = e;
		}
		return pylist;
	}
	return None;
}

void PropertyGrid::setValue(const wxPGProperty * p, pycref pyval) {
	/*
	The built-in types are:
	"bool"
	"char"
	"datetime"
	"double"
	"list"
	"long"
	"longlong"
	"string"
	"ulonglong"
	"arrstring"
	"void*"
	If the variant is null, the value type returned is the string "null" (not the empty string).
	*/

	wxcstr type = p->GetValueType();
	auto &pg = ctrl();

	if (pyval.is_none())
	{
		pg.SetPropertyValue(p, wxNoneString);
		return;
	}

	if (type != "null")
	{
		if (type == "long")
			pg.SetPropertyValue(p, pyval.cast<long>());
		else if (type == "string")
			pg.SetPropertyValue(p, pyval.cast<wxString>());
		else if (type == "bool")
			pg.SetPropertyValue(p, pyval.cast<bool>());
		else if (type == "arrstring") {
			py::list pylist(pyval);
			wxArrayString list;
			list.SetCount(pylist.size());
			int i = 0;
			for (auto &e : pylist)
			{
				list[i++] = pyval.cast<wxString>();
			}
			pg.SetPropertyValue(p, list);
		}
	}
	else
	{
		if (wxIsKindOf(p, wxUIntProperty) || wxIsKindOf(p, wxIntProperty))
			pg.SetPropertyValue(p, pyval.cast<long>());
		else if (wxIsKindOf(p, wxStringProperty) || wxIsKindOf(p, wxLongStringProperty))
			pg.SetPropertyValue(p, pyval.cast<wxString>());
		else if (wxIsKindOf(p, wxBoolProperty))
			pg.SetPropertyValue(p, pyval.cast<bool>());
		else if (wxIsKindOf(p, wxArrayStringProperty)) {
			py::list pylist(pyval);
			wxArrayString list;
			list.SetCount(pylist.size());
			int i = 0;
			for (auto &e : pylist)
			{
				list[i++] = pyval.cast<wxString>();
			}
			pg.SetPropertyValue(p, list);
		}
	}
}

pyobj PropertyGrid::getValues(pycref obj)
{
	pycref data = obj.is_none() ? m_data : obj;

	wxPropertyGridConstIterator it = ctrl().GetIterator();
	for (; !it.AtEnd(); ++it)
	{
		const wxPGProperty* p = *it;
		data[p->GetName()] = getValue(p);
	}
	return data;
}

void PropertyGrid::setValues(pycref data, bool all)
{
	wxString text;

	if (all)
	{
		wxPropertyGridIterator it = ctrl().GetIterator();
		for (; !it.AtEnd(); ++it)
		{
			wxPGProperty* p = *it;
			setValue(p, pyDictGet(data, p->GetName()));
		}
	}
	else
	{
		for (auto &item : data) {
			pystrcpy(text, item);
			wxPGProperty* p = ctrl().GetPropertyByName(text);
			if (p)
			{
				setValue(p, data[item]);
			}
		}
	}
}

void ListView::insertItems(const py::iterable & rows, int pos, bool create)
{
	wxListItem info;
	auto &li = ctrl();
	info.m_mask = wxLIST_MASK_TEXT;
	info.m_itemId = pos != -1 ? pos : li.GetItemCount();
	if (!create && pos == -1)
		create = true;

	for (auto &cols : rows) {
		info.m_col = 0;
		if (create)
			li.InsertItem(info);
		for (auto &item : py::reinterpret_steal<py::iterable>(cols)) {
			pystrcpy(info.m_text, item);
			li.SetItem(info);
			++info.m_col;
		}
		++info.m_itemId;
	}
}
