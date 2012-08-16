## This file is part of Invenio.
## Copyright (C) 2012 CERN.
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

__revision__ = "$Id$"


import os
import re

from invenio.config import CFG_SITE_NAME, \
     CFG_SITE_URL, \
     CFG_SITE_SUPPORT_EMAIL, \
     CFG_SITE_RECORD

from invenio.websubmit_config import CFG_WEBSUBMIT_COPY_MAILS_TO_ADMIN
from invenio.websubmit_functions.Shared_Functions import get_nice_bibsched_related_message, ParamFromFile
from invenio.mailutils import scheduled_send_email
from invenio.bibtask import bibtask_allocate_sequenceid
from invenio.search_engine import get_fieldvalues

def SBI_Mail_Blog_Submitted_to_User(parameters, curdir, form, user_info=None):
    """
    This function sends an email to the user who submitted a blog record
    saying that the blog was successfully submitted

    Parameters:

      * emailFile: Name of the file containing the email of the user

      * titleFile: Name of the file containing the title of the
                   blog record
    """

    global rn, sysno
    FROMADDR = '%s Submission Engine <%s>' % (CFG_SITE_NAME,CFG_SITE_SUPPORT_EMAIL)
    sequence_id = bibtask_allocate_sequenceid(curdir)

    try:
        fp = open("%s/%s" % (curdir,parameters['titleFile']),"r")
        blog_title = fp.read().replace("\n"," ")
        fp.close()
    except:
        blog_title = "-"

    try:
        fp = open("%s/BSI_URL" % curdir,"r")
        blog_url = fp.read().replace ("\n"," ")
        fp.close()
    except:
        blog_url = ""

    # The submitters email address is read from the file specified by 'emailFile'
    try:
        fp = open("%s/%s" % (curdir,parameters['emailFile']),"r")
        m_recipient = fp.read().replace ("\n"," ")
        fp.close()
    except:
        m_recipient = ""

    # create email body
    email_txt = "\nThe blog record with reference number [%s] has been correctly submitted\n\n" % rn
    email_txt += "It will be soon accessible here: <%s/%s/%s>\n" % (CFG_SITE_URL, CFG_SITE_RECORD, sysno)
 
    # email_txt += get_nice_bibsched_related_message(curdir)
    email_txt = email_txt + "\nThank you for using %s Submission Interface.\n" % CFG_SITE_NAME

    email_subject = "Blog record submission done: [%s]" % rn

    ## send the mail, if there are any recipients or copy to admin
    if m_recipient or CFG_WEBSUBMIT_COPY_MAILS_TO_ADMIN:
        scheduled_send_email(FROMADDR, m_recipient.strip(), email_subject, email_txt,
                             copy_to_admin=CFG_WEBSUBMIT_COPY_MAILS_TO_ADMIN,
                             other_bibtasklet_arguments=['-I', str(sequence_id)])

    return ""
