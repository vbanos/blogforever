## This file is part of Invenio.
## Copyright (C) 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""
WebStyle templates. Customize the look of pages of Invenio
"""
__revision__ = \
    "$Id$"

import time
import cgi
import traceback
import urllib
import sys
import string

from invenio.config import \
     CFG_SITE_LANG, \
     CFG_SITE_NAME, \
     CFG_SITE_NAME_INTL, \
     CFG_SITE_SUPPORT_EMAIL, \
     CFG_SITE_SECURE_URL, \
     CFG_SITE_URL, \
     CFG_VERSION, \
     CFG_WEBSTYLE_INSPECT_TEMPLATES, \
     CFG_WEBSTYLE_TEMPLATE_SKIN, \
     CFG_INSPIRE_SITE

from invenio.messages import gettext_set_language, language_list_long, is_language_rtl
from invenio.urlutils import make_canonical_urlargd, create_html_link
from invenio.dateutils import convert_datecvs_to_datestruct, \
                              convert_datestruct_to_dategui
from invenio.bibformat import format_record
from invenio import template
websearch_templates = template.load('websearch')

class Template:

    def tmpl_navtrailbox_body(self, ln, title, previous_links,
                              separator, prolog, epilog):
        """Create navigation trail box body

           Parameters:

          - 'ln' *string* - The language to display

          - 'title' *string* - page title;

          - 'previous_links' *string* - the trail content from site title until current page (both ends exclusive)

          - 'prolog' *string* - HTML code to prefix the navtrail item with

          - 'epilog' *string* - HTML code to suffix the navtrail item with

          - 'separator' *string* - HTML code that separates two navtrail items

           Output:

          - text containing the navtrail

           Note: returns empty string for Home page. (guessed by title).
        """

        # load the right message language
        _ = gettext_set_language(ln)

        out = ""

        if title == CFG_SITE_NAME_INTL.get(ln, CFG_SITE_NAME):
            # return empty string for the Home page
            return out
        else:
            out += create_html_link(CFG_SITE_URL, {'ln': ln},
                                    _("Home"), {'class': 'navtrail'})
        if previous_links:
            if out:
                out += separator
            out += previous_links
        if title:
            if out:
                out += separator
            if title == CFG_SITE_NAME_INTL.get(ln, CFG_SITE_NAME): # hide site name, print Home instead
                out += cgi.escape(_("Home"))
            else:
                out += cgi.escape(title)

        return cgi.escape(prolog) + out + cgi.escape(epilog)

    def tmpl_page(self, req=None, ln=CFG_SITE_LANG, description="",
                  keywords="", userinfobox="", useractivities_menu="",
                  adminactivities_menu="", navtrailbox="",
                  pageheaderadd="", boxlefttop="", boxlefttopadd="",
                  boxleftbottom="", boxleftbottomadd="",
                  boxrighttop="", boxrighttopadd="",
                  boxrightbottom="", boxrightbottomadd="",
                  titleprologue="", title="", titleepilogue="",
                  body="", lastupdated=None, pagefooteradd="", uid=0,
                  secure_page_p=0, navmenuid="", metaheaderadd="",
                  rssurl=CFG_SITE_URL+"/rss",
                  show_title_p=True, body_css_classes=None):

        """Creates a complete page

           Parameters:

          - 'ln' *string* - The language to display

          - 'description' *string* - description goes to the metadata in the header of the HTML page,
                                     not yet escaped for HTML

          - 'keywords' *string* - keywords goes to the metadata in the header of the HTML page,
                                  not yet escaped for HTML

          - 'userinfobox' *string* - the HTML code for the user information box

          - 'useractivities_menu' *string* - the HTML code for the user activities menu

          - 'adminactivities_menu' *string* - the HTML code for the admin activities menu

          - 'navtrailbox' *string* - the HTML code for the navigation trail box

          - 'pageheaderadd' *string* - additional page header HTML code

          - 'boxlefttop' *string* - left-top box HTML code

          - 'boxlefttopadd' *string* - additional left-top box HTML code

          - 'boxleftbottom' *string* - left-bottom box HTML code

          - 'boxleftbottomadd' *string* - additional left-bottom box HTML code

          - 'boxrighttop' *string* - right-top box HTML code

          - 'boxrighttopadd' *string* - additional right-top box HTML code

          - 'boxrightbottom' *string* - right-bottom box HTML code

          - 'boxrightbottomadd' *string* - additional right-bottom box HTML code

          - 'title' *string* - the title of the page, not yet escaped for HTML

          - 'titleprologue' *string* - what to print before page title

          - 'titleepilogue' *string* - what to print after page title

          - 'body' *string* - the body of the page

          - 'lastupdated' *string* - when the page was last updated

          - 'uid' *int* - user ID

          - 'pagefooteradd' *string* - additional page footer HTML code

          - 'secure_page_p' *int* (0 or 1) - are we to use HTTPS friendly page elements or not?

          - 'navmenuid' *string* - the id of the navigation item to highlight for this page

          - 'metaheaderadd' *string* - list of further tags to add to the <HEAD></HEAD> part of the page

          - 'rssurl' *string* - the url of the RSS feed for this page

          - 'show_title_p' *int* (0 or 1) - do we display the page title in the body of the page?

          - 'body_css_classes' *list* - list of classes to add to the body tag

           Output:

          - HTML code of the page
        """

        # load the right message language
        _ = gettext_set_language(ln)

        out = self.tmpl_pageheader(req,
                                   ln = ln,
                                   headertitle = title,
                                   description = description,
                                   keywords = keywords,
                                   metaheaderadd = metaheaderadd,
                                   userinfobox = userinfobox,
                                   useractivities_menu = useractivities_menu,
                                   adminactivities_menu = adminactivities_menu,
                                   navtrailbox = navtrailbox,
                                   pageheaderadd = pageheaderadd,
                                   uid=uid,
                                   secure_page_p = secure_page_p,
                                   navmenuid=navmenuid,
                                   rssurl=rssurl,
                                   body_css_classes=body_css_classes) + """
<div class="pagebody">
  <div class="pagebodystripeleft">
    <div class="pageboxlefttop">%(boxlefttop)s</div>
    <div class="pageboxlefttopadd">%(boxlefttopadd)s</div>
    <div class="pageboxleftbottomadd">%(boxleftbottomadd)s</div>
    <div class="pageboxleftbottom">%(boxleftbottom)s</div>
  </div>
  <div class="pagebodystriperight">
    <div class="pageboxrighttop">%(boxrighttop)s</div>
    <div class="pageboxrighttopadd">%(boxrighttopadd)s</div>
    <div class="pageboxrightbottomadd">%(boxrightbottomadd)s</div>
    <div class="pageboxrightbottom">%(boxrightbottom)s</div>
  </div>
  <div class="pagebodystripemiddle">
    %(titleprologue)s
    %(title)s
    %(titleepilogue)s
    %(body)s
  </div>
  <div class="clear"></div>
</div>
""" % {
  'boxlefttop' : boxlefttop,
  'boxlefttopadd' : boxlefttopadd,

  'boxleftbottom' : boxleftbottom,
  'boxleftbottomadd' : boxleftbottomadd,

  'boxrighttop' : boxrighttop,
  'boxrighttopadd' : boxrighttopadd,

  'boxrightbottom' : boxrightbottom,
  'boxrightbottomadd' : boxrightbottomadd,

  'titleprologue' : titleprologue,
  'title' : (title and show_title_p) and '<div class="headline_div"><h1 class="headline">' + cgi.escape(title) + '</h1></div>' or '',
  'titleepilogue' : titleepilogue,

  'body' : body,

  } + self.tmpl_pagefooter(req, ln = ln,
                           lastupdated = lastupdated,
                           pagefooteradd = pagefooteradd)
        return out

    def tmpl_pageheader(self, req, ln=CFG_SITE_LANG, headertitle="",
                        description="", keywords="", userinfobox="",
                        useractivities_menu="", adminactivities_menu="",
                        navtrailbox="", pageheaderadd="", uid=0,
                        secure_page_p=0, navmenuid="admin", metaheaderadd="",
                        rssurl=CFG_SITE_URL+"/rss", body_css_classes=None):

        """Creates a page header

           Parameters:

          - 'ln' *string* - The language to display

          - 'headertitle' *string* - the title of the HTML page, not yet escaped for HTML

          - 'description' *string* - description goes to the metadata in the header of the HTML page,
                                     not yet escaped for HTML

          - 'keywords' *string* - keywords goes to the metadata in the header of the HTML page,
                                  not yet escaped for HTML

          - 'userinfobox' *string* - the HTML code for the user information box

          - 'useractivities_menu' *string* - the HTML code for the user activities menu

          - 'adminactivities_menu' *string* - the HTML code for the admin activities menu

          - 'navtrailbox' *string* - the HTML code for the navigation trail box

          - 'pageheaderadd' *string* - additional page header HTML code

          - 'uid' *int* - user ID

          - 'secure_page_p' *int* (0 or 1) - are we to use HTTPS friendly page elements or not?

          - 'navmenuid' *string* - the id of the navigation item to highlight for this page

          - 'metaheaderadd' *string* - list of further tags to add to the <HEAD></HEAD> part of the page

          - 'rssurl' *string* - the url of the RSS feed for this page

          - 'body_css_classes' *list* - list of classes to add to the body tag

           Output:

          - HTML code of the page headers
        """

        # load the right message language
        _ = gettext_set_language(ln)

        if body_css_classes is None:
            body_css_classes = []
        body_css_classes.append(navmenuid)

        if CFG_WEBSTYLE_INSPECT_TEMPLATES:
            inspect_templates_message = '''
<table width="100%%" cellspacing="0" cellpadding="2" border="0">
<tr bgcolor="#aa0000">
<td width="100%%">
<font color="#ffffff">
<strong>
<small>
CFG_WEBSTYLE_INSPECT_TEMPLATES debugging mode is enabled.  Please
hover your mouse pointer over any region on the page to see which
template function generated it.
</small>
</strong>
</font>
</td>
</tr>
</table>
'''
        else:
            inspect_templates_message = ""

        sitename = CFG_SITE_NAME_INTL.get(ln, CFG_SITE_NAME)
        if headertitle == sitename:
            pageheadertitle = headertitle
        else:
            pageheadertitle = headertitle + ' - ' + sitename


        out = """\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="%(ln_iso_639_a)s" xml:lang="%(ln_iso_639_a)s" xmlns:og="http://opengraphprotocol.org/schema/" >
<head>
 <title>%(pageheadertitle)s</title>
 <link rev="made" href="mailto:%(sitesupportemail)s" />
 <link rel="stylesheet" href="%(cssurl)s/img/invenio%(cssskin)s.css" type="text/css" />
 <!--[if lt IE 8]>
    <link rel="stylesheet" type="text/css" href="%(cssurl)s/img/invenio%(cssskin)s-ie7.css" />
 <![endif]-->
 <!--[if gt IE 8]>
    <style type="text/css">div.restrictedflag {filter:none;}</style>
 <![endif]-->
 <link rel="alternate" type="application/rss+xml" title="%(sitename)s RSS" href="%(rssurl)s" />
 <link rel="search" type="application/opensearchdescription+xml" href="%(siteurl)s/opensearchdescription" title="%(sitename)s" />
 <link rel="unapi-server" type="application/xml" title="unAPI" href="%(unAPIurl)s" />
 <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
 <meta http-equiv="Content-Language" content="%(ln)s" />
 <meta name="description" content="%(description)s" />
 <meta name="keywords" content="%(keywords)s" />
 <script type="text/javascript" src="%(cssurl)s/js/jquery.min.js"></script>
 %(metaheaderadd)s
</head>
<body%(body_css_classes)s lang="%(ln_iso_639_a)s"%(rtl_direction)s>
<div class="pageheader">
%(inspect_templates_message)s
<!-- replaced page header -->
<div class="headerlogo">
<table class="headerbox" cellspacing="0">
 <tr>
  <td align="right" valign="top" colspan="12">
  <div class="userinfoboxbody">
    %(userinfobox)s
  </div>
  <div class="headerboxbodylogo">
   <a href="%(siteurl)s?ln=%(ln)s">%(sitename)s</a>
  </div>
  </td>
 </tr>
 <tr class="menu">
       <td class="headermoduleboxbodyblank">
             &nbsp;
       </td>
       <td class="headermoduleboxbodyblank">
             &nbsp;
       </td>
       <td class="headermoduleboxbody%(search_selected)s">
             <a class="header%(search_selected)s" href="%(siteurl)s/?ln=%(ln)s">%(msg_search)s</a>
       </td>
       <td class="headermoduleboxbodyblank">
             &nbsp;
       </td>
       <td class="headermoduleboxbody%(submit_selected)s">
             <a class="header%(submit_selected)s" href="%(siteurl)s/submit?ln=%(ln)s">%(msg_submit)s</a>
       </td>
       <td class="headermoduleboxbodyblank">
             &nbsp;
       </td>
       <td class="headermoduleboxbody%(personalize_selected)s">
             %(useractivities)s
       </td>
       <td class="headermoduleboxbodyblank">
             &nbsp;
       </td>
       <td class="headermoduleboxbody%(help_selected)s">
             <a class="header%(help_selected)s" href="%(siteurl)s/help/%(langlink)s">%(msg_help)s</a>
       </td>
       %(adminactivities)s
       <td class="headermoduleboxbodyblanklast">
             &nbsp;
       </td>
 </tr>
</table>
</div>
<table class="navtrailbox">
 <tr>
  <td class="navtrailboxbody">
   %(navtrailbox)s
  </td>
 </tr>
</table>
<!-- end replaced page header -->
%(pageheaderadd)s
</div>
        """ % {
          'rtl_direction': is_language_rtl(ln) and ' dir="rtl"' or '',
          'siteurl' : CFG_SITE_URL,
          'sitesecureurl' : CFG_SITE_SECURE_URL,
          'cssurl' : secure_page_p and CFG_SITE_SECURE_URL or CFG_SITE_URL,
          'cssskin' : CFG_WEBSTYLE_TEMPLATE_SKIN != 'default' and '_' + CFG_WEBSTYLE_TEMPLATE_SKIN or '',
          'rssurl': rssurl,
          'ln' : ln,
          'ln_iso_639_a' : ln.split('_', 1)[0],
          'langlink': '?ln=' + ln,

          'sitename' : CFG_SITE_NAME_INTL.get(ln, CFG_SITE_NAME),
          'pageheadertitle': cgi.escape(pageheadertitle),

          'sitesupportemail' : CFG_SITE_SUPPORT_EMAIL,

          'description' : cgi.escape(description, True),
          'keywords' : cgi.escape(keywords, True),
          'metaheaderadd' : metaheaderadd,

          'userinfobox' : userinfobox,
          'navtrailbox' : navtrailbox,
          'useractivities': useractivities_menu,
          'adminactivities': adminactivities_menu and ('<td class="headermoduleboxbodyblank">&nbsp;</td><td class="headermoduleboxbody%(personalize_selected)s">%(adminactivities)s</td>' % \
          {'personalize_selected': navmenuid.startswith('admin') and "selected" or "",
          'adminactivities': adminactivities_menu}) or '<td class="headermoduleboxbodyblank">&nbsp;</td>',

          'pageheaderadd' : pageheaderadd,
          'body_css_classes' : body_css_classes and ' class="%s"' % ' '.join(body_css_classes) or '',

          'search_selected': navmenuid == 'search' and "selected" or "",
          'submit_selected': navmenuid == 'submit' and "selected" or "",
          'personalize_selected': navmenuid.startswith('your') and "selected" or "",
          'help_selected': navmenuid == 'help' and "selected" or "",

          'msg_search' : _("Search"),
          'msg_submit' : _("Submit"),
          'msg_personalize' : _("Personalize"),
          'msg_help' : _("Help"),
          'languagebox' : self.tmpl_language_selection_box(req, ln),
          'unAPIurl' : cgi.escape('%s/unapi' % CFG_SITE_URL),
          'inspect_templates_message' : inspect_templates_message
        }
        return out

    def tmpl_pagefooter(self, req=None, ln=CFG_SITE_LANG, lastupdated=None,
                        pagefooteradd=""):
        """Creates a page footer

           Parameters:

          - 'ln' *string* - The language to display

          - 'lastupdated' *string* - when the page was last updated

          - 'pagefooteradd' *string* - additional page footer HTML code

           Output:

          - HTML code of the page headers
        """

        # load the right message language
        _ = gettext_set_language(ln)

        if lastupdated and lastupdated != '$Date$':
            if lastupdated.startswith("$Date: ") or \
            lastupdated.startswith("$Id: "):
                lastupdated = convert_datestruct_to_dategui(\
                                 convert_datecvs_to_datestruct(lastupdated),
                                 ln=ln)
            msg_lastupdated = _("Last updated") + ": " + lastupdated
        else:
            msg_lastupdated = ""

        out = """
<div class="pagefooter">
%(pagefooteradd)s
<!-- replaced page footer -->
 <div class="pagefooterstripeleft">
  %(sitename)s&nbsp;::&nbsp;<a class="footer" href="%(siteurl)s/?ln=%(ln)s">%(msg_search)s</a>&nbsp;::&nbsp;<a class="footer" href="%(siteurl)s/submit?ln=%(ln)s">%(msg_submit)s</a>&nbsp;::&nbsp;<a class="footer" href="%(sitesecureurl)s/youraccount/display?ln=%(ln)s">%(msg_personalize)s</a>&nbsp;::&nbsp;<a class="footer" href="%(siteurl)s/help/%(langlink)s">%(msg_help)s</a>
  <br />
  %(msg_poweredby)s <a class="footer" href="http://invenio-software.org/">Invenio</a> v%(version)s
  <br />
  %(msg_maintainedby)s <a class="footer" href="mailto:%(sitesupportemail)s">%(sitesupportemail)s</a>
  <br />
  %(msg_lastupdated)s
 </div>
 <div class="pagefooterstriperight">
  %(languagebox)s
 </div>
<!-- replaced page footer -->
</div>
</body>
</html>
        """ % {
          'siteurl': CFG_SITE_URL,
          'sitesecureurl': CFG_SITE_SECURE_URL,
          'ln': ln,
          'langlink': '?ln=' + ln,

          'sitename': CFG_SITE_NAME_INTL.get(ln, CFG_SITE_NAME),
          'sitesupportemail': CFG_SITE_SUPPORT_EMAIL,

          'msg_search': _("Search"),
          'msg_submit': _("Submit"),
          'msg_personalize': _("Personalize"),
          'msg_help': _("Help"),

          'msg_poweredby': _("Powered by"),
          'msg_maintainedby': _("Maintained by"),

          'msg_lastupdated': msg_lastupdated,
          'languagebox': self.tmpl_language_selection_box(req, ln),
          'version': CFG_VERSION,

          'pagefooteradd': pagefooteradd,
        }
        return out

    def tmpl_language_selection_box(self, req, language=CFG_SITE_LANG):
        """Take URLARGS and LANGUAGE and return textual language
           selection box for the given page.

           Parameters:

          - 'req' - The mod_python request object

          - 'language' *string* - The selected language

        """

        # load the right message language
        _ = gettext_set_language(language)

        # Work on a copy in order not to bork the arguments of the caller
        argd = {}
        if req and req.args:
            argd.update(cgi.parse_qs(req.args))

        parts = []

        for (lang, lang_namelong) in language_list_long():
            if lang == language:
                parts.append('<span class="langinfo">%s</span>' % lang_namelong)
            else:
                # Update the 'ln' argument in the initial request
                argd['ln'] = lang
                if req and req.uri:
                    args = urllib.quote(req.uri, '/:?') + make_canonical_urlargd(argd, {})
                else:
                    args = ""
                parts.append(create_html_link(args,
                                              {}, lang_namelong,
                                              {'class': "langinfo"}))
        if len(parts) > 1:
            return _("This site is also available in the following languages:") + \
                 "<br />" + ' &nbsp;'.join(parts)
        else:
            ## There is only one (or zero?) languages configured,
            ## so there so need to display language alternatives.
            return ""

    def tmpl_error_box(self, ln, title, verbose, req, errors):
        """Produces an error box.

           Parameters:

          - 'title' *string* - The title of the error box

          - 'ln' *string* - The selected language

          - 'verbose' *bool* - If lots of information should be displayed

          - 'req' *object* - the request object

          - 'errors' list of tuples (error_code, error_message)
        """

        # load the right message language
        _ = gettext_set_language(ln)
        info_not_available = _("N/A")

        if title is None:
            if errors:
                title = _("Error") + ': %s' % errors[0][1]
            else:
                title = _("Internal Error")

        browser_s = _("Browser")
        if req:
            try:
                if req.headers_in.has_key('User-Agent'):
                    browser_s += ': ' + req.headers_in['User-Agent']
                else:
                    browser_s += ': ' + info_not_available
                host_s = req.hostname
                page_s = req.unparsed_uri
                client_s = req.remote_ip
            except: # FIXME: bad except
                browser_s += ': ' + info_not_available
                host_s = page_s = client_s = info_not_available
        else:
            browser_s += ': ' + info_not_available
            host_s = page_s = client_s = info_not_available

        error_s = ''
        sys_error_s = ''
        traceback_s = ''
        if verbose >= 1:
            if sys.exc_info()[0]:
                sys_error_s = '\n' + _("System Error") + ': %s %s\n' % \
                              (sys.exc_info()[0], sys.exc_info()[1])
            if errors:
                errs = ''
                for error_tuple in errors:
                    try:
                        errs += "%s%s : %s\n " % (' '*6, error_tuple[0],
                                                  error_tuple[1])
                    except:
                        errs += "%s%s\n" % (' '*6, error_tuple)
                errs = errs[6:-2] # get rid of trainling ','
                error_s = _("Error") + ': %s")' % errs + "\n"
            else:
                error_s = _("Error") + ': ' + info_not_available
        if verbose >= 9:
            traceback_s = '\n' + _("Traceback") + ': \n%s' % \
                          string.join(traceback.format_tb(sys.exc_info()[2]),
                                      "\n")
        out = """
              <table class="errorbox">
                <thead>
                  <tr>
                    <th class="errorboxheader">
                      <p> %(title)s %(sys1)s %(sys2)s</p>
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td class="errorboxbody">
                      <p>%(contact)s</p>
                        <blockquote><pre>
URI: http://%(host)s%(page)s
%(time_label)s: %(time)s
%(browser)s
%(client_label)s: %(client)s
%(error)s%(sys_error)s%(traceback)s
</pre></blockquote>
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <form action="%(siteurl)s/error/send" method="post">
                        %(send_error_label)s
                        <input class="adminbutton" type="submit" value="%(send_label)s" />
                        <input type="hidden" name="header" value="%(title)s %(sys1)s %(sys2)s" />
                        <input type="hidden" name="url" value="URI: http://%(host)s%(page)s" />
                        <input type="hidden" name="time" value="Time: %(time)s" />
                        <input type="hidden" name="browser" value="%(browser)s" />
                        <input type="hidden" name="client" value="Client: %(client)s" />
                        <input type="hidden" name="error" value="%(error)s" />
                        <input type="hidden" name="sys_error" value="%(sys_error)s" />
                        <input type="hidden" name="traceback" value="%(traceback)s" />
                        <input type="hidden" name="referer" value="%(referer)s" />
                      </form>
                    </td>
                  </tr>
                </tbody>
              </table>
              """ % {
                'title'     : cgi.escape(title).replace('"', '&quot;'),
                'time_label': _("Time"),
                'client_label': _("Client"),
                'send_error_label': \
                       _("Please send an error report to the administrator."),
                'send_label': _("Send error report"),
                'sys1'  : cgi.escape(str((sys.exc_info()[0] or ''))).replace('"', '&quot;'),
                'sys2'  : cgi.escape(str((sys.exc_info()[1] or ''))).replace('"', '&quot;'),
                'contact'   : \
                   _("Please contact %s quoting the following information:") % \
                     ('<a href="mailto:' + urllib.quote(CFG_SITE_SUPPORT_EMAIL) +'">' + \
                       CFG_SITE_SUPPORT_EMAIL + '</a>'),
                'host'      : cgi.escape(host_s),
                'page'      : cgi.escape(page_s),
                'time'      : time.strftime("%d/%b/%Y:%H:%M:%S %z"),
                'browser'   : cgi.escape(browser_s).replace('"', '&quot;'),
                'client'    : cgi.escape(client_s).replace('"', '&quot;'),
                'error'     : cgi.escape(error_s).replace('"', '&quot;'),
                'traceback' : cgi.escape(traceback_s).replace('"', '&quot;'),
                'sys_error' : cgi.escape(sys_error_s).replace('"', '&quot;'),
                'siteurl'    : CFG_SITE_URL,
                'referer'   : page_s!=info_not_available and \
                                 ("http://" + host_s + page_s) or \
                                 info_not_available
              }

        return out

    def detailed_record_container_top(self, recid, tabs, ln=CFG_SITE_LANG,
                                      show_similar_rec_p=True,
                                      creationdate=None,
                                      modificationdate=None, show_short_rec_p=True,
                                      citationnum=-1, referencenum=-1, discussionnum=-1):
        """Prints the box displayed in detailed records pages, with tabs at the top.

        Returns content as it is if the number of tabs for this record
        is smaller than 2

           Parameters:

        @param recid: int - the id of the displayed record
        @param tabs: ** - the tabs displayed at the top of the box.
        @param ln: *string* - the language of the page in which the box is displayed
        @param show_similar_rec_p: *bool* print 'similar records' link in the box
        @param creationdate: *string* - the creation date of the displayed record
        @param modificationdate: *string* - the last modification date of the displayed record
        @param show_short_rec_p: *boolean* - prints a very short version of the record as reminder.
        @param citationnum: show (this) number of citations in the citations tab
        @param referencenum: show (this) number of references in the references tab
        @param discussionnum: show (this) number of comments/reviews in the discussion tab
        """
        from invenio.search_engine import record_public_p

        # load the right message language
        _ = gettext_set_language(ln)

        # Prepare restriction flag
        restriction_flag = ''
        if not record_public_p(recid):
            restriction_flag = '<div class="restrictedflag"><span>%s</span></div>' % _("Restricted")

        # If no tabs, returns nothing (excepted if restricted)
        if len(tabs) <= 1:
            return restriction_flag

        # Build the tabs at the top of the page
        out_tabs = ''
        if len(tabs) > 1:
            first_tab = True
            for (label, url, selected, enabled) in tabs:
                addnum = ""
                if (citationnum > -1) and url.count("/citation") == 1:
                    addnum = "(" + str(citationnum) + ")"
                if (referencenum > -1) and url.count("/references") == 1:
                    addnum = "(" + str(referencenum) + ")"
                if (discussionnum > -1) and url.count("/comments") == 1:
                    addnum = "(" + str(discussionnum) + ")"

                css_class = []
                if selected:
                    css_class.append('on')
                if first_tab:
                    css_class.append('first')
                    first_tab = False
                if not enabled:
                    css_class.append('disabled')
                css_class = ' class="%s"' % ' '.join(css_class)
                if not enabled:
                    out_tabs += '<li%(class)s><a>%(label)s %(addnum)s</a></li>' % \
                                {'class':css_class,
                                 'label':label,
                                 'addnum':addnum}
                else:
                    out_tabs += '<li%(class)s><a href="%(url)s">%(label)s %(addnum)s </a></li>' % \
                                {'class':css_class,
                                 'url':url,
                                 'label':label,
                                 'addnum':addnum}
        if out_tabs != '':
            out_tabs = '''        <div class="detailedrecordtabs">
            <div>
                <ul class="detailedrecordtabs">%s</ul>
            <div id="tabsSpacer" style="clear:both;height:0px">&nbsp;</div></div>
        </div>''' % out_tabs


        # Add the clip icon and the brief record reminder if necessary
        record_brief = ''
        if show_short_rec_p:
            record_brief = format_record(recID=recid, of='hs', ln=ln)
            record_brief = '''<div id="detailedrecordshortreminder">
                             <div id="clip">&nbsp;</div>
                             <div id="HB">
                                 %(record_brief)s
                             </div>
                         </div>
                         <div style="clear:both;height:1px">&nbsp;</div>
                         ''' % {'record_brief': record_brief}

        # Print the content
        out = """
    <div class="detailedrecordbox">
        %(tabs)s
        <div class="detailedrecordboxcontent">
            <div class="top-left-folded"></div>
            <div class="top-right-folded"></div>
            <div class="inside">
                <!--<div style="height:0.1em;">&nbsp;</div>
                <p class="notopgap">&nbsp;</p>-->
                %(record_brief)s
                """ % {'tabs':out_tabs,
                       'record_brief':record_brief}

        out = restriction_flag + out

        return out

    def detailed_record_container_bottom(self, recid, tabs, ln=CFG_SITE_LANG,
                                         show_similar_rec_p=True,
                                         creationdate=None,
                                         modificationdate=None, show_short_rec_p=True):
        """Prints the box displayed in detailed records pages, with tabs at the top.

        Returns content as it is if the number of tabs for this record
        is smaller than 2

           Parameters:

         - recid *int* - the id of the displayed record
         - tabs ** - the tabs displayed at the top of the box.
         - ln *string* - the language of the page in which the box is displayed
         - show_similar_rec_p *bool* print 'similar records' link in the box
         - creationdate *string* - the creation date of the displayed record
         - modificationdate *string* - the last modification date of the displayed record
         - show_short_rec_p *boolean* - prints a very short version of the record as reminder.
        """
        # If no tabs, returns nothing
        if len(tabs) <= 1:
            return ''

        # load the right message language
        _ = gettext_set_language(ln)

        similar = ""

        ### BF: let's display a disclaimer with every part of a blog
        from invenio.search_engine_utils import get_fieldvalues
        try:
            coll = get_fieldvalues(recid, "980__a")[0]
        except:
            coll = "record"

        try:
            elem_url = get_fieldvalues(recid, "520__u")[0]
        except:
            elem_url = ""

        elem_html_url = """<a href = '%(url)s'>here</a>""" % {'url': elem_url}

        disclaimer_content = "The content of this %s is an archived copy and not the original, to go to the original click " % coll.lower()

        if show_similar_rec_p and not CFG_INSPIRE_SITE:
            similar = create_html_link(
                websearch_templates.build_search_url(p='recid:%d' % \
                                                     recid,
                                                     rm='wrd',
                                                     ln=ln),
                {}, _("Similar records"),{'class': "moreinfo"})

        out = """
            <div class="bottom-left-folded">%(dates)s</div>
            <div class="bottom-right-folded" style="text-align:right;padding-bottom:2px;">
                <span class="moreinfo" style="margin-right:10px;">%(similar)s</span></div>
            </div>
            <div class="bottom-left-folded">%(disclaimer)s</div>
            </div>
            </div>
            <br/>
    """ % {'similar' : similar,
           'dates' : creationdate and '<div class="recordlastmodifiedbox" style="position:relative;margin-left:1px">&nbsp;%(dates)s</div>' % {
                'dates': _("Record created %(x_date_creation)s, last modified %(x_date_modification)s") % \
                {'x_date_creation': creationdate,
                 'x_date_modification': modificationdate},
                } or '',
           'disclaimer': '<div class="recordlastmodifiedbox" style="position:relative;margin-left:1px">&nbsp;%(disclaimer_content)s  %(url)s</div>' %
                {'disclaimer_content': disclaimer_content,
                 'url': elem_html_url}
           }

        return out


    def detailed_record_mini_panel(self, recid, ln=CFG_SITE_LANG,
                                   format='hd',
                                   files='',
                                   reviews='',
                                   actions=''):
        """Displays the actions dock at the bottom of the detailed record
           pages.

           Parameters:

         - recid *int* - the id of the displayed record
         - ln *string* - interface language code
         - format *string* - the format used to display the record
         - files *string* - the small panel representing the attached files
         - reviews *string* - the small panel representing the reviews
         - actions *string* - the small panel representing the possible user's action
        """
        # load the right message language
        _ = gettext_set_language(ln)

        out = """
        <br />
<div class="detailedrecordminipanel">
<div class="top-left"></div><div class="top-right"></div>
                <div class="inside">

        <div id="detailedrecordminipanelfile" style="width:33%%;float:left;text-align:center;margin-top:0">
             %(files)s
        </div>
        <div id="detailedrecordminipanelreview" style="width:30%%;float:left;text-align:center">
             %(reviews)s
        </div>

        <div id="detailedrecordminipanelactions" style="width:36%%;float:right;text-align:right;">
             %(actions)s
        </div>
        <div style="clear:both;margin-bottom: 0;"></div>
        </div>
        <div class="bottom-left"></div><div class="bottom-right"></div>
        </div>
        """ % {
        'siteurl': CFG_SITE_URL,
        'ln':ln,
        'recid':recid,
        'files': files,
        'reviews':reviews,
        'actions': actions,
        }
        return out

    def tmpl_error_page(self, ln=CFG_SITE_LANG, status="", admin_was_alerted=True):
        """
        Display an error page.

        - status *string* - the HTTP status.
        """
        _ = gettext_set_language(ln)
        out = """
        <p>%(message)s</p>
        <p>%(alerted)s</p>
        <p>%(doubts)s</p>""" % {
            'status' : status,
            'message' : _("The server encountered an error while dealing with your request."),
            'alerted' : admin_was_alerted and _("The system administrators have been alerted.") or '',
            'doubts' : _("In case of doubt, please contact %(x_admin_email)s.") % {'x_admin_email' : '<a href="mailto:%(admin)s">%(admin)s</a>' % {'admin' : CFG_SITE_SUPPORT_EMAIL}}
        }
        return out

    def tmpl_warning_message(self, ln, msg):
        """
        Produces a warning message for the specified text

        Parameters:

          - 'ln' *string* - The language to display the interface in

          - 'msg' *string* - The message to display
        """

        # load the right message language
        _ = gettext_set_language(ln)

        return """<center><font color="red">%s</font></center>""" % msg

    def tmpl_write_warning(self, msg, type='', prologue='', epilogue=''):
        """
        Returns formatted warning message.

        Parameters:

          - 'msg' *string* - The message string

          - 'type' *string* - the warning type

          - 'prologue' *string* - HTML code to display before the warning

          - 'epilogue' *string* - HTML code to display after the warning
        """

        out = '\n%s<span class="quicknote">' % (prologue)
        if type:
            out += '%s: ' % type
        out += '%s</span>%s' % (msg, epilogue)
        return out
