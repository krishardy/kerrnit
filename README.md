# About Kerrnit

Kerrnit is a domain string replacement generator.  This can be used in security research in order to find domains which look similar to domains that you are pentesting.  It works by using character or character-set replacement rules.

This allows you to find domains which are available to register which, due to character kerning, look very similar to the real domains, which you can then use to add some more weight to your social engineering attacks.

You can also pass the -s (or --screenshot) flag, which will use Selenium to visit the website and take a screenshot.

## Example

```bash
$ kerrnit godaddy.com | tee result.txt
Available: goc1acldy.com
Available: gocIaddy.com
Available: gocladdv.com
Available: gocladdy.com
Available: godac1dy.com
Available: godadc1y.com
Available: godacIcly.com
Available: godacldv.com
Available: gocIadcly.com
Available: godac1dv.com
Available: godac1cly.com
Available: godadclv.com
Available: godadcIy.com
Available: godacldy.com
Available: goc1adcly.com
Available: goclacldy.com
Available: goc1addy.com
Available: goc1addv.com
Available: godaclcly.com
Available: godacIdy.com
Available: gocIacldy.com
Available: gocIaddv.com
Available: godadcly.com
Registered, but no IP address: godaddv.com
Available: godacIdv.com
Available: godadc1v.com
Available: godadcIv.com
Available: gocladcly.com
```

```bash
$ kerrnit -s baido.com
bajdo.com screenshots are saved as...
http.bajdo.com.png
https.bajdo.com.png
Available: bajclo.com
Registered, but no IP address: baiclo.com
```
