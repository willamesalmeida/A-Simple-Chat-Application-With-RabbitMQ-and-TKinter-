import pika
import time
from threading import Thread
from tkinter import *
from tkinter import messagebox

def receiver():
    def chamada(ch, method, propreties, body):
        msg_list.insert(END, "Ele: "+ body.decode())
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    
    channel.queue_declare(queue='task_queue1')
    if (channel.basic_consume(queue='task_queue1', on_message_callback= chamada, auto_ack=True)):
        msg_list.insert(END,"Aguarde... ")
        time.sleep(2)
        messagebox.showinfo(" Aviso", "O chat está Ativo!")
        msg_list.delete(0,END)
    channel.start_consuming()
    


def send():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue2')
    live = entry_field.get()     
    msg_list.insert(END, "Você: " + live)
    
    channel.basic_publish(exchange='', routing_key='task_queue2', body= live)    
    connection.close()


#instancia da TK (janela)

janela = Tk()
janela.title("Chat 2")
janela.geometry("350x300+700+100")

#Botões, envia e sair

send_button = Button(janela, text= "Send", command= send)
send_button.pack(side = BOTTOM, anchor = S, pady = 10)


#BOTAO SAIR DEVE CHAMAR A FUNÇAO CLOSE PARA DESCONECTAR 

botao_sair = Button(janela, text = "Sair", command= janela.destroy)
botao_sair.pack(side = TOP, anchor = NE, pady = 5, padx = 5)

#Recebe os valores do usuario com a caixa de texto

entry_field = Entry(janela, textvariable = '')
#entry_field.bind("<Return>", send)
entry_field.pack(side = BOTTOM, anchor = S,pady=  10)

#Apresenta o texto na tela  

messages_frame = Frame(janela)       
scrollbar = Scrollbar(messages_frame) 
msg_list = Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side= RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH)
msg_list.pack()
messages_frame.pack()

receive_thread = Thread(target= receiver)
sender_thread = Thread(target= send)
receive_thread.start()
sender_thread.start()
janela.mainloop()