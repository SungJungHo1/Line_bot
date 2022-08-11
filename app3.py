# -*- coding: utf-8 -*-
import os
import sys

from linebot import (
    LineBotApi,
)

from linebot.models import (
    RichMenu,
    RichMenuArea,
    RichMenuSize,
    RichMenuBounds,
    URIAction
)
from linebot.models.actions import RichMenuSwitchAction
from linebot.models.rich_menu import RichMenuAlias

channel_access_token = "LPoD2xZWE8Yz/OiZvghUhnuVRWqijmXiziipqaGKLbr30u9nEYmn3gcXM+U41brU6fKNWFMEcEyAQi/KiDaHHLHB/CJBbRphNIJLAYgmNJ6R18csA3uCr/IlGOGNZZIOsHmjTgH2gF4wSSI5/NRROQdB04t89/1O/w1cDnyilFU="
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)


def rich_menu_object_a_json(id):
    return {
        "size": {
            "width": 2500,
            "height": 1686
        },
        "selected": True,
        "name": "taiFood",
        "chatBarText": "Tap to open",
        "areas": [
            {
                "bounds": {
                    "x": 0,
                    "y": 0,
                    "width": 1250,
                    "height": 1686
                },
                "action": {
                    "type": "uri",
                    "uri": f"https://www.tmxkqjrtm.kr/?id={id}"
                }
            },
            {
                "bounds": {
                    "x": 1251,
                    "y": 0,
                    "width": 1250,
                    "height": 1686
                },
                "action": {
                    "type": "uri",
                    "uri":f"https://www.go.com/?id={id}",
                }
            }
        ]
    }


def create_action(action):
    if action['type'] == 'uri':
        return URIAction(type=action['type'], uri=action.get('uri'))
    else:
        return RichMenuSwitchAction(
            type=action['type'],
            rich_menu_alias_id=action.get('richMenuAliasId'),
            data=action.get('data')
        )


def main(id):
    # 2. Create rich menu A (richmenu-a)
    rich_menu_object_a = rich_menu_object_a_json(id)
    areas = [
        RichMenuArea(
            bounds=RichMenuBounds(
                x=info['bounds']['x'],
                y=info['bounds']['y'],
                width=info['bounds']['width'],
                height=info['bounds']['height']
            ),
            action=create_action(info['action'])
        ) for info in rich_menu_object_a['areas']
    ]

    rich_menu_to_a_create = RichMenu(
        size=RichMenuSize(width=rich_menu_object_a['size']['width'],
                          height=rich_menu_object_a['size']['height']),
        selected=rich_menu_object_a['selected'],
        name=rich_menu_object_a['name'],
        chat_bar_text=rich_menu_object_a['name'],
        areas=areas
    )

    rich_menu_a_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_a_create)

    # 3. Upload image to rich menu A
    with open('./public/richmenu-a.png', 'rb') as f:
        line_bot_api.set_rich_menu_image(rich_menu_a_id, 'image/png', f)

    # 7. Create rich menu alias A
    alias_a = RichMenuAlias(
        rich_menu_alias_id='richmenu-alias-a',
        rich_menu_id=rich_menu_a_id
    )
    # line_bot_api.delete_rich_menu_alias("richmenu-alias-a")
    # line_bot_api.create_rich_menu_alias(alias_a)
    line_bot_api.link_rich_menu_to_user(user_id=
        id,rich_menu_id=rich_menu_a_id)

    print('success')

if __name__ == "__main__":
    main("Uad859360a7e2589c8c213b3b47fc27a2")
