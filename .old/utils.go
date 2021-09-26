package main

import (
	"github.com/labstack/echo"
	"html/template"
	"io"
)

type TemplateRenderer struct {
	templates *template.Template
}

// Render renders a template document
func (t *TemplateRenderer) Render(w io.Writer, name string, data interface{}, c echo.Context) error {
	if viewContext, isMap := data.(map[string]interface{}); isMap { // Add global methods if data is a map

		viewContext["reverse"] = c.Echo().Reverse
	}

	return t.templates.ExecuteTemplate(w, name, data)
}

func Render(path string) *TemplateRenderer {
	return &TemplateRenderer{
		templates: template.Must(template.ParseGlob(path)),
	}
}

// String to HTML. Not really used much.
//func HTML(html string) template.HTML {
//	return template.HTML(html)
//}
