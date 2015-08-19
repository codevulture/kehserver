# -*- coding: utf-8 -*-
# try something like
import gluon.contenttype
import datetime

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

def register():
    username = request.vars.username
    password = request.vars.password
    email = request.vars.email
    dob = datetime.datetime.strptime(request.vars.dob, "%Y%m%d").date()

    row = db.auth_user(username = username)
    if not row:
        user = db.auth_user.validate_and_insert(username = username, password = password, email = email, dob = dob)
        if not user.id == None:
            return gluon.contrib.simplejson.dumps({'result': user})
            #return returnResultTrue()
        else:
            return returnResultFalse()
    else:
        raise HTTP(409, 'username exists')

def login():
    username = request.vars.username
    password = request.vars.password

    user = auth.login_bare(username,password)
    if not user:
        return gluon.contrib.simplejson.dumps({'result': False})
    return returnUser(user)

def loginfailed(*args):
    raise HTTP(409, 'autorization failed') 

auth.settings.on_failed_authentication = loginfailed

def verifyuser():
    username = request.vars.username
    user = db(db.auth_user.username == username).select()
    import gluon.contrib.simplejson
    try:
        user[0]
        return returnUser(user[0])
    except:
        return returnResultFalse()

def verifyuseremail():
    useremail = request.vars.useremail
    user = db(db.auth_user.email == useremail).select()
    import gluon.contrib.simplejson
    try:
        user[0]
        return returnUser(user[0])
    except:
        return returnResultFalse()

@auth.requires_login()
def addvedioboard():
    user = auth.user
    board_name = request.vars.name
    icon = int(request.vars.board_icon_id)
    try:
        db.video_board.insert(board_name = board_name, user_d = user, icon_id = icon)
        return returnResultTrue()
    except:
        return returnResultFalse()

@auth.requires_login()
def addvideo():
    user = auth.user
    name = request.vars.video_title
    thumbnail = request.vars.thumbnail
    video = request.vars.video
    
    tags = gluon.contrib.simplejson.loads(request.vars.tags)

    #try:
    video = db.video.insert(name = name, user_d = user, thumbnail = db.video.thumbnail.store(thumbnail.file, thumbnail.filename), \
                                thumbnail_blob = thumbnail.file.read(), video = db.video.video.store(video.file, video.filename), video_blob = video.file.read())
    '''
        for tag in tags:
            t = tag.id
            if t == -1:
                t = db.tag.insert(name = tag.text)
            db.tag.insert(tag = t, video = video)
    '''
    return returnResultTrue()
    #except:
    #    return returnResultFalse()


@auth.requires_login()
def markfavorite():
    user = auth.user
    video = request.vars.videoid
    state = request.vars.favorite
    try:
        if not state:
            record = db((db.favrioute.user_d == user) & (db.favrioute.video == video)).delete()
        else:
            db.favrioute.insert(vedio, user = user)
        return returnResultTrue()
    except:
        return returnResultFalse()

@auth.requires_login()
def getmyvideos():
    user = auth.user

    videos = [v.id for v in db(db.video.user_d == user).select()]
    return getVideo(videos, user)


@auth.requires_login()
def addvideotoboard():
    user = auth.user
    board = request.vars.board_id
    video = request.vars.video_id
    #try:
    board = db(db.video_board.id == board).select()[0]
    video = db(db.video.id == video).select()[0]
    db.video_board_item.insert(video_board = board, video = video)
    return gluon.contrib.simplejson.dumps({'result': True})
    #except:
    #    return gluon.contrib.simplejson.dumps({'result': False})

@auth.requires_login()
def getuserboards():
    user = auth.user
    #try:
    row = db(db.video_board.user_d == user).select()
    return gluon.contrib.simplejson.dumps({'board_list':[{'board_id': r.id, 'board_name': r.board_name, 'username': r.user_d, 'board_icon_id': r.icon_id} for r in row]})
    #except:
    #    return gluon.contrib.simplejson.dumps({'result': False})

'''
def getboardvideos():
    board = int(request.vars.boardid)
    try:
        row = db(db.video_board_item.video_board == board).select()
'''
'''
@service.jsonrpc
def addtag(tag, vedio):
    try:
        tag = db(db.tag.tag == tag).select()
        vedio = db(db.vedio.id == vedio).select()
        db.tag_item.insert(tag = tag, vedio = vedio)
        return {'result': True}
    except:
        return {'result': False}
'''