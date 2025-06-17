import os
import sys
import time
import random
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {   #移動用辞書
    pg.K_UP: (0,-5),
    pg.K_DOWN: (0,+5),
    pg.K_LEFT: (-5,0),
    pg.K_RIGHT: (+5,0),
}
DELTA2 = {
    
}   #移動用辞書

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct:pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：横方向判定結果，縦方向判定結果
    画面内ならTrue,画面外ならFalse
    """
    yoko, tate = True, True#初期値:画面の中
    if rct.left < 0 or WIDTH < rct.right:#横方向の画面外判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:#縦方向の画面外判定
        tate = False
    return yoko, tate#横方向,縦方向の画面内判定結果を返す


def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー
    Game Overの文字実装
    こうかとんの実装
    """
    back_rect = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(back_rect, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT)) #対応するsurface , 色, 表示位置
    screen.blit(back_rect, [0, 0])
    fonto = pg.font.Font(None, 70)#文字のサイズ変更
    txt = fonto.render("GameOver", True, (255, 255, 255))
    rct =txt.get_rect()#文字の表示範囲の取得
    rct.center = WIDTH/2,HEIGHT/2    #取得した表示範囲から文字の位置の設定
    screen.blit(txt, rct)
    kk2_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 1.5) #こうかとんの大きさの設定
    screen.blit(kk2_img, [300, HEIGHT/2-50])#こうかとんの位置の設定1
    screen.blit(kk2_img, [750, HEIGHT/2-50])#こうかとんの位置の設定2
    pg.display.update()
    time.sleep(5)
    return


def  init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    爆弾のサイズと加速度の段階的なリストを生成して返す関数
    戻り値:
    爆弾Surfaceのリスト（サイズ1〜10段階）
    対応する加速度リスト（1〜10）
    """
    bb_imgs = []

    bb_accs = [a for a in range(1, 11)]  # 加速度：1〜10段階
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))  # サイズは20×倍率
        bb_img.set_colorkey((0, 0, 0))     # 黒を透明色に設定
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)  # 赤い円
        bb_imgs.append(bb_img)
    return bb_imgs, bb_accs

def load_kk_images() -> dict[tuple[int, int], pg.Surface]:
    """
    各方向の移動ベクトルに対応するこうかとん画像を読み込んで辞書で返す

    戻り値:
        {(dx, dy): Surface} の辞書（こうかとんの向き画像）
    """
    
    return kk_images

    




def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_images = load_kk_images()  # こうかとん画像辞書の初期化
    kk_img = kk_images[(0, -1)]   # 初期は上向き画像
    kk_rct.center = 300, 200
    
    bb_img = pg.Surface((20,20)) #空のSurfaseを作る(爆弾用)
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)#赤い円を描く
    bb_img.set_colorkey((0,0,0))#黒を透明色に設定
    bb_rct = bb_img.get_rect()#爆弾rectを取得
    bb_rct.centerx = random.randint(0,WIDTH)#横座標用乱数
    bb_rct.centery = random.randint(0,HEIGHT)#縦座標用乱数
    vx, vy = +5, +5#爆弾の移動速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        if kk_rct.colliderect(bb_rct):#こうかとんRectと爆弾Rectの衝突判定
            gameover(screen)
            print("ゲームオーバー")
            return
        
        bb_imgs, bb_accs = init_bb_imgs()
        avx = vx * bb_accs[min(tmr//500, 9)]
        avy = vy * bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        vx == avx#加速した速さに置き換える
        vy == avy#加速した速さに置き換える

        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
            kk_img = load_kk_images(tuple(sum_mv), kk_images)  # ← 向きの画像に差し替え
            screen.blit(kk_img, kk_rct)

        

        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key,mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])#移動をなかったことにする
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(avx,avy)#爆弾の移動
        yoko, tate = check_bound(bb_rct)
        if not yoko:#横方向にはみ出ていたら
            vx *= -1
        if not tate:#縦方向にはみ出ていたら
            vy *= -1
        screen.blit(bb_img, bb_rct)#爆弾の描画
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
