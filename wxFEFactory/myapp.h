#pragma once

#include <wx/wx.h>

class MyApp: public wxApp
{
public:
	bool OnInit() override;
	int OnExit() override;
};

DECLARE_APP(MyApp)