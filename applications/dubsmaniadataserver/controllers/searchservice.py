# -*- coding: utf-8 -*-
# try something like
import gluon.contenttype

def gettrendingvideos():
    region = request.vars.region
    start = int(request.vars.start)
    end = int(request.vars.end)
    user = request.vars.user
    user = db(db.auth_user.username == user).select()[0]
    #return gluon.contrib.simplejson.dumps({'result': True})

    #try:
    region = db(db.d_region.f_region == region).select()[0]
    videos = [v.video for v in db(db.trending_vedio.f_region == region).select(db.trending_vedio.video)] #limitby=(start,end))]
    return getVideo(videos, user)

def getvideo():
    id = request.vars.id
    import gluon.contenttype
    #try:
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.mp4')
    row = db(db.video.id == id).select(db.video.video).first()
    filename, file = db.video.video.retrieve(row.video)
    return file.read()
    #except:
    return gluon.contrib.simplejson.dumps({'result': 'error'})

def getfavoritvideos():
    user = request.vars.user
    video = [fav.video for fav in db(db.favriouts.user_d == user).select(db.favriouts.video)]
    return getVideo(videos, user)


def getboardvideos():
    board = int(request.vars.board_id)
    user = request.vars.user
    if user == None:
        user = ""
    
    user = db(db.auth_user.username == user).select()[0]
    
    videos = [v.video for v in db(db.video_board_item.video_board == board).select(db.video_board_item.video)]
    return getVideo(videos, user)


def gettrendingvedioboard():
    region = request.vars.region
    start = int(request.vars.start)
    end = int(request.vars.end)
    user = request.vars.user    
    return db(db.trending_board).select(limitby=(start,end))

def gettags():
    row = db(db.tag).select()
    return gluon.contrib.simplejson.dumps({'tags':[{'id': r.id, 'tagname': r.tag} for r in row]})

def seachbytag(tag):
    tags = request.vars.tags
    tag = db(db.tag.tag == tag).select()
    return db(db.vedio.id == tag.id).select()
