import pyxel
import random

class White: #上から降りてくるボール

    def __init__(self):
      self.syoutai = random.choice([5,6,9])
      self.white_y = 0
      self.white_x = 100
      self.white_direction = True # True: 右方向 False: 左方向
      self.colchange = False 
      self.tekilong = 0
      self.habatu = "kinoko"
      self.teki = "takenoko"


    def moveWhite(self):

      self.white_y += 2

      if self.white_x > 200:
        self.white_direction = False
      elif self.white_x < 0:
        self.white_direction = True

      if self.white_direction:
        self.white_x += 1
      else:
        self.white_x -= 1

      if self.white_y == 200 or self.white_y == 0:
        self.white_y = 0
        self.white_x = random.randint(10, 190)
        self.colchange = False 
        self.tekilong += 1
      

class Player: #プレイヤー

  def __init__(self):
    self.player_x = pyxel.mouse_x 
    self.ball_kazu = 16
    self.ball_x = self.player_x
    self.ball_y = 200 
    self.hakolong = 1
    self.pstate = 1
    self.balldraw = False
    

  def ball(self):
    self.balldraw = True
    self.ball_x = self.player_x
    self.ball_y -= 10 
   
    if self.ball_y <= 0:
      self.balldraw = False
      self.ball_y = 200


  def ballkazu(self):

    if self.ball_kazu  != 0:
      self.ball_kazu -= 1
    else:
      self.pstate = 2   #App.checkStateにて変換


class App:
  
  def __init__(self):
    pyxel.init(200,200)
    self.state = 0 
    # 0: スタート画面 1: ゲーム中 2: ゲームオーバー 3:ゲームクリア
    self.col = 4
    self.text = "??"
    pyxel.run(self.update, self.draw)


  def update(self):

    if self.state == 0: #0: スタート画面 

      if pyxel.btnp(pyxel.KEY_1):
        App.make(self)
        App.plmake(self)
        self.w.habatu = "kinoko"
        self.w.teki = "takenoko"
        self.state = 1


      if pyxel.btnp(pyxel.KEY_2):
        App.make(self)
        App.plmake(self)
        self.w.habatu = "takenoko"
        self.w.teki = "kinoko"
        self.state = 1
          

    elif self.state == 1: #1: ゲーム中 

        self.p.player_x = pyxel.mouse_x
        self.w.moveWhite() #White動く
        self.checkState() # ゲームオーバクリア判定
        self.wbhit() #white-ball当たり判定
        self.wphit() #white-player当たり判定
        
           
        if pyxel.btnp(pyxel.KEY_SPACE):
          self.p.ballkazu()
          self.p.balldraw = True
          
        if self.p.balldraw == True:
          self.p.ball()

    elif self.state == 2: #2: ゲームオーバー
      if pyxel.btnp(pyxel.KEY_RETURN):  
        self.state = 0 


    elif self.state == 3: #2: ゲームクリア
      if pyxel.btnp(pyxel.KEY_RETURN):  
        self.state = 0 


  def make(self): 
    self.w = White()


  def plmake(self):
    self.p = Player()


  def checkState(self): 
    #self.p.pstate == 2とは、検証ボール数が0になるということ。
    if self.p.pstate == 2 or self.p.hakolong == 0 or self.w.tekilong == 14: #ユーザー表示されるのは7
      self.state = 2 #ゲームオーバー

    if self.p.hakolong == 7: 
      self.state = 3 #ゲームクリア

  def wbhit(self): #white-ball当たり判定
    if (self.w.white_y - 20  <= self.p.ball_y and self.w.white_y + 20 >= self.p.ball_y) and (self.w.white_x - 20  <= self.p.ball_x and self.w.white_x + 20 >= self.p.ball_x):
      
      self.w.colchange = True
      # self.w.yuka = False

      if self.p.hakolong <= 3:
        if self.w.habatu == "kinoko":
          self.w.syoutai = random.choice([5,5,5,6,9])
        if self.w.habatu == "takenoko":
          self.w.syoutai = random.choice([5,6,9,9,9])
      else:
          self.w.syoutai = random.choice([5,6,9])
  

  def wphit(self): #white-player当たり判定
    if self.w.white_x - 20  <= self.p.player_x and self.w.white_x + 20 >= self.p.player_x:

      if self.p.hakolong >= 1 and (self.w.white_y - 20  <= 180 and self.w.white_y + 20 >= 180):
        self.atari()
      if self.p.hakolong >= 2 and (self.w.white_y - 20  <= 150 and self.w.white_y + 20 >= 150):
        self.atari()
      if self.p.hakolong >= 3 and (self.w.white_y - 20  <= 120 and self.w.white_y + 20 >= 120):
        self.atari()

    if (self.p.hakolong >= 4) and ((self.w.white_x - 20  <= self.p.player_x and self.w.white_x + 20 >= self.p.player_x) or (self.w.white_x - 20  <= self.p.player_x + 30 and self.w.white_x + 20 >= self.p.player_x + 30)):

      if self.p.hakolong >= 4 and (self.w.white_y - 20  <= 180 and self.w.white_y + 20 >= 180):
        self.atari()
      if self.p.hakolong >= 5 and (self.w.white_y - 20  <= 150 and self.w.white_y + 20 >= 150):
        self.atari()
      if self.p.hakolong >= 6 and (self.w.white_y - 20  <= 120 and self.w.white_y + 20 >= 120):
        self.atari()


  def atari(self):

        if self.p.hakolong != 3:
          if self.p.hakolong != 6: #短絡評価？対策

              if self.col == self.pcol: 
                  self.p.hakolong += 1 
                  self.w.white_y = 0
                  self.w.colchange = False 
                  
              elif self.col != self.pcol and self.col != 7:       
                self.p.hakolong -= 1 
                self.w.white_y = 0
                self.w.colchange = False

            
          else: #6とき

              if self.text == "Nonce":
                self.p.hakolong += 1 
                self.w.white_y = 0
                self.w.colchange = False 

              else:
                self.p.hakolong -= 1 
                self.w.white_y = 0
                self.w.colchange = False

        else: #3とき

              if self.text == "Nonce":
                self.p.hakolong += 1 
                self.p.ball_kazu += 5 #マイニング報酬！
                self.w.white_y = 0
                self.w.colchange = False 

              else:
                self.p.hakolong -= 1 
                self.w.white_y = 0
                self.w.colchange = False

              
  def draw(self):

    pyxel.cls(7)
    if self.state == 0:
      pyxel.text(60, 70, "kinoko:1 ,takenoko:2", 0)

    elif self.state == 1:
    
      # White 
      if self.w.habatu == "kinoko": #後でキノコ白に。
        self.pcol = 5
      else:
        self.pcol = 9


      if self.p.hakolong != 3:
        if self.p.hakolong != 6: #短絡評価？対策

          if self.w.colchange == True:
              
              if self.w.syoutai == 5:
                self.col = 5
              elif self.w.syoutai ==  6:
                self.col = 6
              else:
                self.col = 9

          elif self.w.colchange == False:

              self.col = 4

          pyxel.circ(self.w.white_x, self.w.white_y, 10, self.col)
        
        else: #6の時
          if self.w.colchange == True:
              
              if self.w.syoutai == 6: 
                self.text = "Nonce"
              elif self.w.syoutai ==  5:
                self.text = "Web3"
              else:
                self.text = "SFC"

          elif self.w.colchange == False:
              
              self.text = "??"

          pyxel.text(self.w.white_x, self.w.white_y, self.text, self.pcol)
        
      else: #3の時
          if self.w.colchange == True:
              # self.state = 2
              if self.w.syoutai == 6: #レア！
                self.text = "Nonce"
              elif self.w.syoutai ==  5:
                self.text = "Web3"
              else:
                self.text = "SFC"

          elif self.w.colchange == False:
              # and self.w.yuka == True
              self.text = "??"

          pyxel.text(self.w.white_x, self.w.white_y, self.text, self.pcol)


      # Player(TX)
      if self.p.hakolong >= 1:
        pyxel.circ(self.p.player_x, 180, 15, self.pcol)
      if self.p.hakolong >= 2:
        pyxel.circ(self.p.player_x, 150, 15, self.pcol)
      if self.p.hakolong >= 3:
        pyxel.circ(self.p.player_x, 120, 15, self.pcol) 
      if self.p.hakolong >= 4:
        pyxel.rect(self.p.player_x -15, 105, 32, 105, self.pcol)
        pyxel.text(self.p.player_x ,125, "B", 7)
        pyxel.text(self.p.player_x ,135, "l", 7)
        pyxel.text(self.p.player_x ,145, "o", 7)
        pyxel.text(self.p.player_x ,155, "c", 7)
        pyxel.text(self.p.player_x ,165, "k", 7)
        pyxel.circ(self.p.player_x + 30, 180, 15, self.pcol) 
      if self.p.hakolong >= 5:
        pyxel.circ(self.p.player_x + 30, 150, 15, self.pcol) 
      if self.p.hakolong >= 6:
        pyxel.circ(self.p.player_x + 30, 120, 15, self.pcol) 

      #pBall(検証ボール)
      #ball_y更新！！
      if self.p.balldraw == True:
        pyxel.circ(self.p.ball_x, self.p.ball_y, 15, self.pcol) 


      # 残りボール（と条件シーンごとのメッセージ）
      pyxel.text(10, 10, "ball: " + str(self.p.ball_kazu), 0)
      pyxel.text(10, 20, self.w.teki + " - long: " + str(self.w.tekilong // 2), 0)
      # 2回落ちたら相手の長さ１つ増える。商を表示。

      if self.p.hakolong == 3:
        pyxel.text(70, 80, "Look for Nonce !!!!", 0)
      if self.p.hakolong == 6:
        pyxel.text(70, 80, "Look for Nonce !!!!", 0)

    if self.state == 2:
      pyxel.text(60, 70, "You LOSE", 0)
      pyxel.text(60, 80, "Press Enter to Restart", 0)

    if self.state == 3:
      pyxel.text(60, 70, "You WIN", 4)
      pyxel.text(60, 80, "Press Enter to Restart", 0)

App() # プログラム実行時にはここが呼ばれる
