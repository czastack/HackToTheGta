#include <wx/wx.h>
#include "layoutbase.h"


wxVector<Layout*> View::LAYOUTS;

View::View(pycref key, pycref className, pycref style)
	:m_key(key), m_class(className), m_style(style)
{
	if (py::isinstance<py::str>(m_class) && m_class.contains(" "))
	{
		m_class = m_class.attr("split")(" ");
	}
	Layout* pLayout = getActiveLayout();
	if (pLayout)
	{
		// �����ʽ��
		auto styles_list = pLayout->getStylesList();
		if (styles_list)
		{
			for (auto e : *styles_list)
			{
				testStyles(py::reinterpret_borrow<py::object>(e));
			};
		}
	}
}

void View::addToParent() {
	Layout* pLayout = getActiveLayout();
	if (pLayout)
	{
		pLayout->add(*this);
	}
}

wxWindow* View::safeActiveWindow()
{
	Layout *layout = getActiveLayout();
	return layout ? layout->ptr() : wxGetApp().GetTopWindow();
}

void View::addStyle(pyobj style)
{
	pyobj tmp;
	if (py::isinstance<py::list>(m_style))
	{
		// ׷��
		tmp = m_style;
	}
	else {
		// ���б�
		py::list tmpList = py::list();
		if (!m_style.is_none())
		{
			tmpList.append(m_style);
		}
		tmp = tmpList;
	}
	py::list tmpList = tmp.cast<py::list>();
	if (py::isinstance<py::list>(style))
	{
		tmpList.attr("extend")(style);
	}
	else
	{
		tmpList.append(style);
	}
	m_style = tmpList;
}

pyobj View::getStyle(wxcstr key)
{
	if (py::isinstance<py::list>(m_style))
	{
		static auto reversed = py::module::import("builtins").attr("reversed");
		auto tmp = reversed(m_style);
		pyobj pykey = py::str(key);
		PyObject* ret;

		for (auto &e : tmp)
		{
			ret = PyDict_GetItem(e.ptr(), pykey.ptr());
			if (ret)
			{
				return py::reinterpret_borrow<py::object>(ret);
			}
		}
		return None;
	}
	return pyDictGet(m_style, key);
}

bool View::hasStyle(pyobj & key)
{
	if (py::isinstance<py::list>(m_style))
	{
		for (auto &e : m_style)
		{
			if (e != None && e.contains(key))
			{
				return true;
			}
		}

		return false;
	}
	return m_style != None && m_style.contains(key);
}

/**
* ����Ӧ����ʽ��
*/

void View::testStyles(pycref styles)
{
	pycref typecase = pyDictGet(styles, wxT("type"), None);
	pycref classcase = pyDictGet(styles, wxT("class"), None);

	pyobj style = pyDictGet(typecase, getTypeName());
	if (!style.is_none())
	{
		addStyle(style);
	}
	if (py::isinstance<py::list>(m_class))
	{
		for (auto &e : m_class)
		{
			style = pyDictGet(classcase, py::reinterpret_borrow<py::object>(e));
			if (!style.is_none())
			{
				addStyle(style);
			}
		}
	}
	else
	{
		style = pyDictGet(classcase, m_class);
		if (!style.is_none())
		{
			addStyle(style);
		}
	}
}

void View::applyStyle()
{
	pyobj style;

	style = getStyle(STYLE_BACKGROUND);
	if (style != None)
	{
		if (py::isinstance<py::str>(style))
		{
			setBackground(parseColor(style.cast<wxString>(), m_elem->GetBackgroundColour().GetRGB()));
		}
		else {
			setBackground(style.cast<int>());
		}
	}

	style = getStyle(STYLE_COLOR);
	if (style != None)
	{
		if (py::isinstance<py::str>(style))
		{
			setForeground(parseColor(style.cast<wxString>(), m_elem->GetForegroundColour().GetRGB()));
		}
		else {
			setForeground(style.cast<int>());
		}
	}

	style = getStyle(STYLE_FONTSIZE);
	if (style != None)
	{
		wxFont font = m_elem->GetFont();
		font.SetPointSize(style.cast<int>());
		m_elem->SetFont(font);
	}

	style = getStyle(STYLE_FONT);
	if (style != None)
	{
		wxFont font = m_elem->GetFont();

		// ����
		wxcstr weightStr = pyDictGet(style, wxT("weight"), wxNoneString);
		if (weightStr != wxNoneString)
		{
			font.SetWeight(
				weightStr == wxT("normal") ? wxFONTWEIGHT_NORMAL :
				weightStr == wxT("light") ? wxFONTWEIGHT_LIGHT :
				weightStr == wxT("bold") ? wxFONTWEIGHT_BOLD :
				font.GetWeight()
			);
		}

		// ������ʽ
		wxcstr styleStr = pyDictGet(style, wxT("style"), wxNoneString);
		if (styleStr != wxNoneString)
		{
			font.SetStyle(
				styleStr == wxT("normal") ? wxFONTSTYLE_NORMAL :
				styleStr == wxT("italic") ? wxFONTSTYLE_ITALIC :
				styleStr == wxT("slant") ? wxFONTSTYLE_SLANT :
				font.GetStyle()
			);
		}

		font.SetUnderlined(pyDictGet(style, wxT("underline"), false));
		font.SetFaceName(pyDictGet(style, wxT("face"), wxNoneString));

		m_elem->SetFont(font);
	}

	if (hasStyle(STYLE_MINWIDTH) || hasStyle(STYLE_MINHEIGHT))
	{
		wxSize size = m_elem->GetMinSize();
		style = getStyle(STYLE_MINWIDTH);
		if (style != None)
			size.SetWidth(style.cast<int>());
		style = getStyle(STYLE_MINHEIGHT);
		if (style != None)
			size.SetHeight(style.cast<int>());
		m_elem->SetMinSize(size);
	}

	if (hasStyle(STYLE_MAXWIDTH) || hasStyle(STYLE_MAXHEIGHT))
	{
		wxSize size = m_elem->GetMaxSize();
		style = getStyle(STYLE_MAXWIDTH);
		if (style != None)
			size.SetWidth(style.cast<int>());
		style = getStyle(STYLE_MAXHEIGHT);
		if (style != None)
			size.SetHeight(style.cast<int>());
		m_elem->SetMaxSize(size);
	}
}

Layout* View::getParent()
{
	auto elemParent = m_elem->GetParent();
	void *parent = elemParent ? (Layout*)elemParent->GetClientData() : nullptr;
	if (parent)
	{
		if (Item::isInstance(parent))
		{
			parent = ((Item*)parent)->getView();
		}
	}
	return (Layout*)parent;
}

pyobj Layout::__enter__() {
	LAYOUTS.push_back(this);

	Layout *parent = getParent();
	tmp_styles_list = new wxVector<PyObject*>;

	bool only_self = false; // ��Ԫ�ص���ʱ�б���û�ͷţ�����ֻҪ����Լ���
	if (parent && parent->tmp_styles_list)
	{
		for (auto e : *parent->tmp_styles_list)
		{
			tmp_styles_list->push_back(e);
		}
		only_self = true;
	}

	parent = this;
	while (parent) {
		if (!parent->m_styles.is_none())
		{
			if (py::isinstance<py::list>(parent->m_styles))
			{
				for (auto &e : parent->m_styles)
				{
					if (e != None)
						tmp_styles_list->push_back(e.ptr());
				}
			}
			else if (parent->m_styles != None)
			{
				tmp_styles_list->push_back(parent->m_styles.ptr());
			}
		}

		if (only_self)
			break;

		parent = parent->getParent();
	}

	return py::cast(this);
}

void Layout::__exit__(py::args & args) {
	LAYOUTS.pop_back();

	for (auto &e : m_children)
	{
		View &child = *py::cast<View*>(e);
		if (!child.beforeAdded())
		{
			continue;
		}

		if (!child.getKey().is_none())
		{
			m_named_children[child.getKey()] = py::cast(&child);
		}
		child.applyStyle();
		doAdd(child);
	}

	// �ͷ���ʱ��ʽ��
	delete tmp_styles_list;
	tmp_styles_list = nullptr;
}

void Layout::setStyles(pycref styles)
{
	m_styles = styles;

	if (!styles.is_none())
	{
		for (auto &child : m_children)
		{
			py::cast<View*>(child)->testStyles(styles);
		}
	}
	reLayout();
}