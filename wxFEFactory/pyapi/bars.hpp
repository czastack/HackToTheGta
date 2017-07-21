#pragma once
#include <wx/sharedptr.h>
#include "layoutbase.hpp"
#include <wx/artprov.h>

class ToolBar : public Control
{
public:
	template <class... Args>
	ToolBar(Args ...args) : Control(args...)
	{
		bindElem(new wxToolBar(*safeActiveLayout(), wxID_ANY, wxDefaultPosition, getStyleSize(), wxTB_DEFAULT_STYLE | wxTB_TEXT));
		m_ctrl().Bind(wxEVT_COMMAND_TOOL_CLICKED, &ToolBar::onClick, this);
	}

	ToolBar& addTool(wxcstr label, wxcstr shortHelp, wxcstr bitmap, pycref onclick, int toolid, wxcstr kind)
	{
		wxBitmap bp = wxArtProvider::GetBitmap(wxART_GO_BACK, wxART_TOOLBAR);

		if (!bitmap.IsEmpty())
		{
			bp.LoadFile(bitmap, wxBITMAP_TYPE_PNG);
		}
		wxToolBarToolBase *tool = m_ctrl().AddTool(toolid, label, bp, shortHelp, getItemKind(kind));
		m_listeners[py::cast(tool->GetId())] = onclick;
		return *this;
	}

	ToolBar& addSeparator() {
		m_ctrl().AddSeparator();
		return *this;
	}

	ToolBar& realize() {
		m_ctrl().Realize();
		return *this;
	}

	void clear()
	{
		m_ctrl().ClearTools();
	}

	void onClick(wxCommandEvent &event)
	{
		pycref onclick = pyDictGet(m_listeners, py::cast(event.GetId()));
		if (!onclick.is_none())
		{
			pyCall(onclick, py::cast(this), event.GetId());
		}
	}

	void setToolText(int id, wxcstr label)
	{
		wxToolBarToolBase *tool = m_ctrl().FindById(id);
		tool->SetLabel(label);
	}

protected:
	py::dict m_listeners;

	wxToolBar& m_ctrl()
	{
		return *(wxToolBar*)m_elem;
	}
};


class StatusBar : public Control
{
public:
	template <class... Args>
	StatusBar(Args ...args) : Control(args...)
	{
		Layout &layout = *safeActiveLayout();
		bindElem(new wxStatusBar(layout));
		if (wxIsKindOf(layout.ptr(), wxFrame))
		{
			((wxFrame*)layout.ptr())->SetStatusBar((wxStatusBar*)m_elem);
		}
		else
		{
			log_message("StatusBar must be child of Window");
		}
	}

	wxString getText(int n) const
	{
		return m_ctrl().GetStatusText(n);
	}

	StatusBar& setText(wxcstr text, int n)
	{
		m_ctrl().SetStatusText(text, n);
		return *this;
	}

	StatusBar& setFieldsCount(pycref list)
	{
		int n;
		auto ptr = asArray<int>(list, n);
		m_ctrl().SetFieldsCount(n, ptr.get());
		return *this;
	}

	StatusBar& setItemWidths(pycref list)
	{
		int n;
		auto ptr = asArray<int>(list, n);
		m_ctrl().SetStatusWidths(n, ptr.get());
		return *this;
	}

	int getStatusWidth(int n) const
	{
		return m_ctrl().GetStatusWidth(n);
	}

	void popStatusText(int n)
	{
		m_ctrl().PopStatusText(n);
	}

	void pushStatusText(wxcstr text, int n)
	{
		m_ctrl().PushStatusText(text, n);
	}

protected:
	wxStatusBar& m_ctrl() const
	{
		return *(wxStatusBar*)m_elem;
	}
};