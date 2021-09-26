package main

import (
	"fmt"
	"github.com/labstack/echo"
	"net/http"
	"strings"
)

func registerGetHandler(c echo.Context) error {
	return c.Render(http.StatusOK, "search.html", map[string]interface{}{
		"title": "test",
	})
}

var letters = []rune("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

func searchPostHandler(c echo.Context) error {
	var out []string
	domain := strings.Split(c.FormValue("query"), ".")[0]

	for _, tld := range config.TLDs { // for tld in tlds...
		out = append(out, domain+"."+tld)
	}

	return c.JSON(http.StatusOK, out)
}

func registerPostHandler(c echo.Context) error {
	domain := c.FormValue("domain")

	if isValid(domain) && !Registered(domain) {
		token := token()
		Add(domain, Domain{domain, token, nil})
		return c.JSON(http.StatusOK, map[string]interface{}{ // If domain is valid...
			"domain": domain,
			"token":  token,
		})
	} else {
		return c.JSON(http.StatusOK, map[string]interface{}{ // TODO: What status code?
			"message": "Domain not available",
		})
	}
}

func recordDeleteHandler(c echo.Context) error {
	var token string
	if len(c.Request().Header["Token"]) != 1 {
		return c.JSON(http.StatusUnauthorized, map[string]interface{}{
			"message": "token header not found.",
		})
	} else {
		token = c.Request().Header["Token"][0]
	}
	domain := c.Param("domain")
	record := c.Param("record")

	fmt.Printf(record)

	if Registered(domain) && Get(domain).Token == token { // and record exists.
		//TODO: delete the entry
		return c.JSON(http.StatusOK, map[string]interface{}{
			"message": "Delete Success",
		})
	} else {
		return c.JSON(http.StatusUnauthorized, map[string]interface{}{
			"message": "Invalid token",
		})
	}
}

func recordCreateHandler(c echo.Context) error {
	var token string
	if len(c.Request().Header["Token"]) != 1 {
		return c.JSON(http.StatusUnauthorized, map[string]interface{}{
			"message": "token header not found.",
		})
	} else {
		token = c.Request().Header["Token"][0]
	}

	domain := c.Param("domain")
	rname := c.Param("record")
	rtype := c.FormValue("type")
	rvalue := c.FormValue("value")

	if Registered(domain) && Get(domain).Token == token { // and record exists.
		Add(domain, Domain{domain, token, append(Get(domain).Records, Record{rtype, rname, rvalue})})
		return c.JSON(http.StatusOK, map[string]interface{}{
			"message": "Delete Success",
		})
	} else {
		return c.JSON(http.StatusUnauthorized, map[string]interface{}{
			"message": "Invalid token",
		})
	}
}

func main() {
	e := echo.New()
	e.Renderer = Render("templates/*.html")

	e.POST("/search", searchPostHandler)
	e.GET("/search", registerGetHandler)
	e.File("/register", "templates/register.html")

	e.POST("/register", registerPostHandler)

	e.DELETE("/edit/:domain/:record", recordDeleteHandler)
	e.POST("/edit/:domain/:record", recordCreateHandler)

	e.Logger.Fatal(e.Start(config.Host + ":" + config.Port))
}
