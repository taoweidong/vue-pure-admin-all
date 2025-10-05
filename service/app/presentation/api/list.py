from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.database.database import get_db
from app.presentation.api.dependencies import get_current_user

router = APIRouter()


@router.post("/get-card-list")
async def get_card_list(
    request: dict,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取卡片列表"""
    try:
        # 模拟卡片数据
        card_list = [
            {
                "index": 1,
                "isSetup": True,
                "type": 4,
                "banner": "https://tdesign.gtimg.com/tdesign-pro/cloud-server.jpg",
                "name": "SSL证书",
                "description": "SSL证书又叫服务器证书，腾讯云为您提供证书的一站式服务，包括免费、付费证书的申请、管理及部"
            },
            {
                "index": 2,
                "isSetup": False,
                "type": 4,
                "banner": "https://tdesign.gtimg.com/tdesign-pro/t-sec.jpg",
                "name": "人脸识别",
                "description": "SSL证书又叫服务器证书，腾讯云为您提供证书的一站式服务，包括免费、付费证书的申请、管理及部"
            },
            {
                "index": 3,
                "isSetup": False,
                "type": 5,
                "banner": "https://tdesign.gtimg.com/tdesign-pro/ssl.jpg",
                "name": "CVM",
                "description": "云硬盘为您提供用于CVM的持久性数据块级存储服务。云硬盘中的数据自动地可用区内以多副本冗"
            },
            {
                "index": 4,
                "isSetup": False,
                "type": 2,
                "banner": "https://tdesign.gtimg.com/tdesign-pro/ssl.jpg",
                "name": "SSL证书",
                "description": "云数据库MySQL为用户提供安全可靠，性能卓越、易于维护的企业级云数据库服务。"
            },
            {
                "index": 5,
                "isSetup": True,
                "type": 3,
                "banner": "https://tdesign.gtimg.com/tdesign-pro/face-recognition.jpg",
                "name": "SSL证书",
                "description": "云数据库MySQL为用户提供安全可靠，性能卓越、易于维护的企业级云数据库服务。"
            }
        ]
        
        return {
            "success": True,
            "data": {
                "list": card_list
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get-async-routes")
async def get_async_routes(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取异步路由"""
    try:
        # 根据用户角色返回不同的路由
        user_roles = getattr(current_user, 'user_roles', [])
        is_admin = any(ur.role.code == 'admin' for ur in user_roles if ur.role)
        
        # 系统管理路由
        system_management_router = {
            "path": "/system",
            "meta": {
                "icon": "ri:settings-3-line",
                "title": "menus.pureSysManagement",
                "rank": 10
            },
            "children": [
                {
                    "path": "/system/user/index",
                    "name": "SystemUser",
                    "meta": {
                        "icon": "ri:admin-line",
                        "title": "menus.pureUser",
                        "roles": ["admin"]
                    }
                },
                {
                    "path": "/system/role/index",
                    "name": "SystemRole",
                    "meta": {
                        "icon": "ri:admin-fill",
                        "title": "menus.pureRole",
                        "roles": ["admin"]
                    }
                },
                {
                    "path": "/system/menu/index",
                    "name": "SystemMenu",
                    "meta": {
                        "icon": "ep:menu",
                        "title": "menus.pureSystemMenu",
                        "roles": ["admin"]
                    }
                },
                {
                    "path": "/system/dept/index",
                    "name": "SystemDept",
                    "meta": {
                        "icon": "ri:git-branch-line",
                        "title": "menus.pureDept",
                        "roles": ["admin"]
                    }
                }
            ]
        }

        # 系统监控路由
        system_monitor_router = {
            "path": "/monitor",
            "meta": {
                "icon": "ep:monitor",
                "title": "menus.pureSysMonitor",
                "rank": 11
            },
            "children": [
                {
                    "path": "/monitor/online-user",
                    "component": "monitor/online/index",
                    "name": "OnlineUser",
                    "meta": {
                        "icon": "ri:user-voice-line",
                        "title": "menus.pureOnlineUser",
                        "roles": ["admin"]
                    }
                },
                {
                    "path": "/monitor/login-logs",
                    "component": "monitor/logs/login/index",
                    "name": "LoginLog",
                    "meta": {
                        "icon": "ri:window-line",
                        "title": "menus.pureLoginLog",
                        "roles": ["admin"]
                    }
                },
                {
                    "path": "/monitor/operation-logs",
                    "component": "monitor/logs/operation/index",
                    "name": "OperationLog",
                    "meta": {
                        "icon": "ri:history-fill",
                        "title": "menus.pureOperationLog",
                        "roles": ["admin"]
                    }
                },
                {
                    "path": "/monitor/system-logs",
                    "component": "monitor/logs/system/index",
                    "name": "SystemLog",
                    "meta": {
                        "icon": "ri:file-search-line",
                        "title": "menus.pureSystemLog",
                        "roles": ["admin"]
                    }
                }
            ]
        }

        # 权限管理路由
        permission_router = {
            "path": "/permission",
            "meta": {
                "title": "menus.purePermission",
                "icon": "ep:lollipop",
                "rank": 9
            },
            "children": [
                {
                    "path": "/permission/page/index",
                    "name": "PermissionPage",
                    "meta": {
                        "title": "menus.purePermissionPage",
                        "roles": ["admin", "common"]
                    }
                },
                {
                    "path": "/permission/button",
                    "name": "PermissionButton",
                    "meta": {
                        "title": "menus.purePermissionButton",
                        "roles": ["admin", "common"]
                    }
                }
            ]
        }

        # 标签页路由
        tabs_router = {
            "path": "/tabs",
            "meta": {
                "icon": "ri:bookmark-2-line",
                "title": "menus.pureTabs",
                "rank": 12
            },
            "children": [
                {
                    "path": "/tabs/index",
                    "name": "Tabs",
                    "meta": {
                        "title": "menus.pureTabs",
                        "roles": ["admin", "common"]
                    }
                }
            ]
        }

        # 外部页面路由
        iframe_router = {
            "path": "/iframe",
            "meta": {
                "icon": "ri:links-fill",
                "title": "menus.pureExternalPage",
                "rank": 7
            },
            "children": [
                {
                    "path": "/iframe/external",
                    "name": "PureIframeExternal",
                    "meta": {
                        "title": "menus.pureExternalDoc",
                        "roles": ["admin", "common"]
                    },
                    "children": [
                        {
                            "path": "/external",
                            "name": "https://pure-admin.cn/",
                            "meta": {
                                "title": "menus.pureExternalLink",
                                "roles": ["admin", "common"]
                            }
                        },
                        {
                            "path": "/pureUtilsLink",
                            "name": "https://pure-admin-utils.netlify.app/",
                            "meta": {
                                "title": "menus.pureUtilsLink",
                                "roles": ["admin", "common"]
                            }
                        }
                    ]
                },
                {
                    "path": "/iframe/embedded",
                    "name": "PureIframeEmbedded",
                    "meta": {
                        "title": "menus.pureEmbeddedDoc",
                        "roles": ["admin", "common"]
                    },
                    "children": [
                        {
                            "path": "/iframe/ep",
                            "name": "FrameEp",
                            "meta": {
                                "title": "menus.pureEpDoc",
                                "frameSrc": "https://element-plus.org/zh-CN/",
                                "roles": ["admin", "common"]
                            }
                        }
                    ]
                }
            ]
        }

        # 根据用户角色返回不同的路由
        routes = []
        if is_admin:
            routes.extend([
                iframe_router,
                permission_router,
                system_management_router,
                system_monitor_router,
                tabs_router
            ])
        else:
            routes.extend([
                iframe_router,
                permission_router,
                tabs_router
            ])

        return {
            "success": True,
            "data": routes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))