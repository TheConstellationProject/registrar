package main

import (
	"fmt"
	"github.com/labstack/echo"
	"math/rand"
	"net/http"
	"strings"
)

//func registerGetHandler(c echo.Context) error {
//	return c.Render(http.StatusOK, "register.html", map[string]interface{}{})
//}

var letters = []rune("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

func token() string {
	b := make([]rune, 64) // 64 characters
	for i := range b {
		b[i] = letters[rand.Intn(len(letters))]
	}
	return string(b)
}

func inTLDs(tld string) bool {
	for _, ptld := range config.TLDs { // for tld in tlds...
		if ptld == tld {
			return true
		}
	}
	return false
}

func searchPostHandler(c echo.Context) error {
	var out []string
	domain := strings.Split(c.FormValue("query"), ".")[0]

	for _, tld := range config.TLDs { // for tld in tlds...
		out = append(out, domain+"."+tld)
	}

	return c.JSON(http.StatusOK, out)
}

func isValid(domain string) bool {
	pdomain := strings.Split(domain, ".")
	return len(pdomain) == 2 && inTLDs(pdomain[1])
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

	e.POST("/register", registerPostHandler)

	e.DELETE("/edit/:domain/:record", recordDeleteHandler)
	e.POST("/edit/:domain/:record", recordCreateHandler)

	e.Logger.Fatal(e.Start(config.Host + ":" + config.Port))
}
