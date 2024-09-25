import tkinter as tk
from tkinter import messagebox
import math

# Oyun tahtasını başlat
board = [' ' for _ in range(9)]
current_player = 'X'

# Oyunun GUI penceresini oluştur
root = tk.Tk()
root.title("Tic-Tac-Toe")

# Tahtayı temizle
def reset_board():
    global board, current_player
    board = [' ' for _ in range(9)]
    current_player = 'X'
    update_buttons()
    for button in buttons:
        button.config(state="normal")

# Oyun tahtasındaki butonlara tıklama fonksiyonu
def button_click(index):
    global current_player
    if board[index] == ' ':
        board[index] = current_player
        update_buttons()
        if winner(current_player):
            messagebox.showinfo("Kazanan!", f"{current_player} kazandı!")
            disable_buttons()
        elif not empty_squares():
            messagebox.showinfo("Berabere!", "Oyun berabere bitti!")
            disable_buttons()
        else:
            if current_player == 'X':
                current_player = 'O'
                ai_move()
                current_player = 'X'
    else:
        messagebox.showwarning("Geçersiz Hamle", "Bu kare zaten dolu!")

# Kazananı kontrol eden fonksiyon
def winner(player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Yatay
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Dikey
        [0, 4, 8], [2, 4, 6]              # Çapraz
    ]
    for condition in win_conditions:
        if board[condition[0]] == player and board[condition[1]] == player and board[condition[2]] == player:
            return True
    return False

# AI'nin hamle yapması
def ai_move():
    if empty_squares():
        best_move = minimax('O')['position']
        board[best_move] = 'O'
        update_buttons()
        if winner('O'):
            messagebox.showinfo("Kazanan!", "O kazandı!")
            disable_buttons()
        elif not empty_squares():
            messagebox.showinfo("Berabere!", "Oyun berabere bitti!")
            disable_buttons()

# Butonları güncelleme
def update_buttons():
    for i, button in enumerate(buttons):
        button.config(text=board[i])

# Tüm karelerin boş olup olmadığını kontrol etme
def empty_squares():
    return ' ' in board

# Butonları devre dışı bırakma
def disable_buttons():
    for button in buttons:
        button.config(state="disabled")

# Minimax algoritması
def minimax(player):
    max_player = 'O'
    other_player = 'X' if player == 'O' else 'O'
    
    if winner(other_player):
        return {'position': None, 'score': 1 * (len(available_moves()) + 1) if other_player == max_player else -1 * (len(available_moves()) + 1)}
    elif not empty_squares():
        return {'position': None, 'score': 0}

    if player == max_player:
        best = {'position': None, 'score': -math.inf}
    else:
        best = {'position': None, 'score': math.inf}

    for possible_move in available_moves():
        board[possible_move] = player
        sim_score = minimax(other_player)
        board[possible_move] = ' '

        sim_score['position'] = possible_move

        if player == max_player:
            if sim_score['score'] > best['score']:
                best = sim_score
        else:
            if sim_score['score'] < best['score']:
                best = sim_score

    return best

# Mevcut hamlelerin bulunduğu indeksleri döner
def available_moves():
    return [i for i, spot in enumerate(board) if spot == ' ']

# Oyun tahtası butonlarını oluştur
buttons = []
for i in range(9):
    button = tk.Button(root, text=' ', font=('Arial', 20), width=5, height=2,
                       command=lambda i=i: button_click(i))
    button.grid(row=i//3, column=i%3)
    buttons.append(button)

# Reset butonu
reset_button = tk.Button(root, text="Yeniden Başlat", font=('Arial', 14), command=reset_board)
reset_button.grid(row=3, column=0, columnspan=3)

# Oyun döngüsü
root.mainloop()
