import re
def gl(cont):
    RLST = []
    for x in re.findall(r'(\[\[([^\[\]])+?]]|{{([^{}]+?)}})',cont):
        Lcont = x[0]
        PLNK = re.search(r'^\[\[([^|#]+)(?:#([^|]+))?.*?]]$',Lcont)
        if PLNK != None:
            try:
                SNAME = PLNK.group(2)
                SECTION = ("#{}".format(SNAME)) if SNAME != None else ""
            except IndexError:
                SECTION = ""
            RLST.append(PLNK.group(1) + SECTION)
            continue
        FUNC = re.search(r'^{{ *#(exer|if|ifeq|ifexist|ifexpr|switch|time|language|babel|invoke) *:',Lcont)
        if FUNC != None:
            RLST.append("mw:Help:Extension:ParserFunctions#{}".format(FUNC))
            continue
        TND = re.search(r'^{{ *(?:subst:|safesubst:)?(?:CURRENTYEAR|CURRENTMONTH|CURRENTMONTHNAME|CURRENTMONTHNAMEGEN|CURRENTMONTHABBREV|CURRENTDAY|CURRENTDAY2|CURRENTDOW|CURRENTDAYNAME|CURRENTTIME|CURRENTHOUR|CURRENTWEEK|CURRENTTIMESTAMP|LOCALYEAR|LOCALMONTH|LOCALMONTHNAME|LOCALMONTHNAMEGEN|LOCALMONTHABBREV|LOCALDAY|LOCALDAY2|LOCALDOW|LOCALDAYNAME|LOCALTIME|LOCALHOUR|LOCALWEEK|LOCALTIMESTAMP) .*}}$',Lcont)
        if TND != None:
            RLST.append("mw:Help:Magic_words#Date_and_time")
            continue
        TMD = re.search(r'^{{ *(?:subst:|safesubst:)?(?:SITENAME|SERVER|SERVERNAME|DIRMARK|DIRECTIONMARK|SCRIPTPATH|CURRENTVERSION|CONTENTLANGUAGE|CONTENTLANG) .*}}$',Lcont)
        TMDS = TMD if TMD != None else re.search(r'^{{ *(?:subst:|safesubst:)?(?:NUMBEROFPAGES|NUMBEROFARTICLES|NUMBEROFFILES|NUMBEROFEDITS|NUMBEROFVIEWS|NUMBEROFUSERS|NUMBEROFADMINS|NUMBEROFACTIVEUSERS|PAGESINCATEGORY|PAGESINCAT|PAGESINCATEGORY|PAGESINCATEGORY|PAGESINCATEGORY|PAGESINCATEGORY|NUMBERINGROUP|NUMBERINGROUP|PAGESINNS|PAGESINNAMESPACE)([:|].+?)?}}$',Lcont)
        if TMDS != None:
            RLST.append("mw:Help:Magic_words#Technical_metadata")
            continue
        STAT = re.search(r'^{{ *(?:subst:|safesubst:)?(?:NUMBEROFPAGES|NUMBEROFARTICLES|NUMBEROFFILES|NUMBEROFEDITS|NUMBEROFVIEWS|NUMBEROFUSERS|NUMBEROFADMINS|NUMBEROFACTIVEUSERS|PAGESINCATEGORY|PAGESINCAT|PAGESINCATEGORY|PAGESINCATEGORY|PAGESINCATEGORY|PAGESINCATEGORY|NUMBERINGROUP|NUMBERINGROUP|PAGESINNS|PAGESINNAMESPACE)([:|].+?)?}}$',Lcont)
        if STAT != None:
            RLST.append("mw:Help:Magic_words#Statistics")
            continue
        PTIT = re.search(r'^{{ *(?:subst:|safesubst:)?(?:FULLPAGENAME|PAGENAME|BASEPAGENAME|SUBPAGENAME|SUBJECTPAGENAME|TALKPAGENAME|FULLPAGENAMEE|PAGENAMEE|BASEPAGENAMEE|SUBPAGENAMEE|SUBJECTPAGENAMEE|TALKPAGENAMEE)(:.+?)?}}$',Lcont)
        if PTIT != None:
            RLST.append("mw:Help:Magic_words#Page_names")
            continue
        NS = re.search(r'^{{ *(?:subst:|safesubst:)?(?:NAMESPACE|SUBJECTSPACE|ARTICLESPACE|TALKSPACE|NAMESPACEE|SUBJECTSPACEE|TALKSPACEE)(:.+?)?}}$',Lcont)
        if NS != None:
            RLST.append("mw:Help:Magic_words#Namespaces")
            continue
        OTH = re.search(r'^{{ *! *}}$',Lcont)
        if OTH != None:
            RLST.append("mw:Help:Magic_words#Other")
            continue
        URLD = re.search(r'^{{ *(localurl|fullurl|filepath|urlencode|anchorencode):.+}}$',Lcont)
        if URLD != None:
            RLST.append("mw:Help:Magic_words#URL_data")
            continue
        NSII = re.search(r'^{{ *(localurl|fullurl|filepath|urlencode|anchorencode):.+}}$',Lcont)
        if NSII != None:
            RLST.append("mw:Help:Magic_words#Namespaces_2")
            continue
        FORMAT = re.search(r'^{{ *(?:subst:|safesubst:)?(lc|lcfirst|uc|ucfirst|formatnum|#dateformat|#formatdate|padleft|padright|plural):.+}}$',Lcont)
        if FORMAT != None:
            RLST.append("mw:Help:Magic_words#Formatting")
            continue
        MISC = re.search(r'^{{ *(int|#special|#tag|gender|PAGEID|noexternallanglinks)(:.+)?}}$',Lcont)
        if MISC != None:
            RLST.append("mw:Help:Magic_words#Miscellaneous")
            continue
        TEMP = re.search(r'^{{ *(?:subst:|safesubst:)?([^|]+)(?:|.+)?}}$',Lcont)
        if TEMP != None:
            RLST.append("Template:{}".format(TEMP.group(1)))
            continue
    return RLST
        
        
        
