#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, time, json, urllib, urllib2, threading
import argparse
from os.path import dirname, realpath

try:
    # install
    import kitty
except ImportError, e:
    # local
    sys.path.append(dirname(dirname(realpath(__file__))))
    import kitty

#================================ head end ====================================

# logger = root

class ImgPress(threading.Thread):

    def __init__(self, id, site, query_list):
        threading.Thread.__init__(self)
        self.id = id
        self.site = site
        self.queryList = query_list

    def run(self):
        logger.notice("thread: %d start", self.id)
        start_time = time.time()
        etime = time.time() + 1
        for query in self.queryList:

            url = "http://%s/i?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1401980826979_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=gbk&oe=utf-8&word=%s&rn=30&pn=0" % (self.site, urllib.quote(query))
            try:
                ret = urllib2.urlopen(url, timeout=10)
            except urllib2.HTTPError, e :
                logger.warning("HTTPError code: %d", e.code)
                
            except urllib2.URLError, e :
                logger.warning("URLError reason: %s", e.reason)

            ntime = time.time()
            if ntime < etime :
                time.sleep(etime - ntime)
            etime = etime + 1
        end_time = time.time()

        logger.notice("thread: %d finished use[%f]", self.id, end_time - start_time)

    def stop(self):
        self.thread_stop = True


def doPress(site, file_path, n) :
    file_in = open(file_path, 'r')
    start_time = time.time()

    query_list = [];
    for line in file_in :
        query = line.strip()
        query_list.append(query)

    file_in.close()

    query_len = len(query_list)
    sub_len = query_len / n
    for i in xrange(0,n):
        start = i * sub_len
        end = start + sub_len
        end = end if end < query_len else query_len
        l = query_list[start:end]
        sub_thread = ImgPress(i, site ,l)
        sub_thread.start()



def getImageJsonStr(site, query, pn) :
    url = "http://%s/i?tn=baiduimagejson&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1401980826979_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=gbk&oe=utf-8&word=%s&rn=90&pn=%d" % (site, urllib.quote(query) , pn)
    try:
        ret = urllib2.urlopen(url, timeout=10).read()
    except urllib2.HTTPError, e :
        logger.warning("HTTPError code: %d", e.code)
        return False
    except urllib2.URLError, e :
        logger.warning("URLError reason: %s", e.reason)
        return False
    return ret


def parseJson(str, pn, file_out) :
    decodejson = json.loads(str)
    if empty(decodejson) :
        print "1"
        return False

    if not 'data' in decodejson:
        print "2"
        return False

    if empty(decodejson['data']):
        print "3"

        return False

    length = len(decodejson['data'])
    for i in xrange(0,length):
        if empty(decodejson['data'][i]) :
            break;
        objurl = decodejson['data'][i]['objURL']
        fromurl = decodejson['data'][i]['fromURL']
        file_out.write("%s\t%d\t%s\t%s\n"%(query, pn, objurl.encode('utf-8'), fromurl.encode('utf-8')))

    return True


# =============================================================================
def main():

    file_in  = open("./query", 'r')
    file_out = open("./out", 'w')

    for line in file_in :
        query = line.strip()
        pn = 0
        json_str = getImageJsonStr("10.46.128.23:8090", query, pn)
        if not json_str :
            print "getImageJsonStr error, query[%s]"%(query)
            continue
        # print json_str
        if not parseJson(json_str, pn, file_out) :
            print "parseJson error, query[%s]"%(query)
            continue
    file_in.close()
    filt_out.close()

def opt_parse():
    parser = argparse.ArgumentParser(description='this is a spider')
    parser.add_argument('file',
                        help='query list file path')
    parser.add_argument('-p', action='store', dest='velocity', type=int, default=20,
                        help='request velocity(per second), default 20')
    args = parser.parse_args()
    return args

if __name__ == "__main__" :
    global logger

    args = opt_parse()
    
    app_name = 'spider'
    kitty.setup(app_name, "bin.settings")

    from kitty.utils.log import getLogger

    logger = getLogger(app_name)

    logger.notice('start')
    # doPress('10.46.128.15:8090', args.file, args.velocity)
    


