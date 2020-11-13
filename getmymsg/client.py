#!/usr/bin/env python

import signal
import socket
import logging
import hashlib
import threading
import time
import socket
import re
import base64
from .config import Config


class IdentificationException(Exception):
	"""
	Exception para primer paso de protocolo
	"""
	def __init__(self):
                self.error = "No se logro establecer la identificacion del usuario."

class MsglenException(Exception):
	"""
	Exception para msglen establishment
	"""
	def __init__(self):
		self.error = "No se logro establecer el MsgLen."

class GiveMsgException(Exception):
        """
        Exception para entrega del mensaje
        """
        def __init__(self):
                self.error = "No se logro obtener el mensaje"

class ChkMsgException(Exception):
        """
        Exception para msglen establishment
        """
        def __init__(self):
                self.error = "No se logro obtener el mensaje"

class ByeCmdException(Exception):
	"""
	Exception para el cierre de la conexion con el servidor
	"""
	def __init__(self):
		self.error = "No se logro cerrar la conexion con el servidor"

class ConnectionException(Exception):
        """
        Exception para conexion con el servidor
        """
        def __init__(self):
                self.error = "No se logro realizar la conexion con el servidor"

###Clase para establecer parametros a futuro, no esta en uso en esta version
class Params(object):
    """
    Estructura de un objeto Commnad
    """
    def __init__(self, data):
        self.__params = []
        proc_data = data.strip('\n').strip('\r').split(' ')
        for part in proc_data:
            if part == '':
                continue
            else:
                self.__params.append(part)

    @property
    def params(self):
        return self.__params


class Client():

	IDENTIFICATION_CMD = 'helloiam '
	MSGLEN_CMD = 'msglen'
	GIVEMEMSG_CMD = 'givememsg '
	CHKMSG_CMD = 'chkmsg '
	BYE_CMD = 'bye'
	
	def __init__(self):
		self.__conf = None
		self.__sock = None

	def config(self)
		if self.__conf is None:
			self.__conf = Config()
		return self.__conf

	@property
	def client_sock(self):
		if self.__sock is None:
			socket.setdefaulttimeout(2.0)
			self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		return self.__sock
	
	@property
	def msgudp_sock(self):
		if self.__udpsock is None:
			socket.setdefaulttimeout(2.0)
			self.__udpsock = socket.socket(socket.AF_INET, SOCK_DGRAM)
		return self__udpsock
	
	@property
    	def on_work(self):
        	return self.__working


	def prepare(self):
	        """
        	Preparación del servidor
        	"""
        	addr = self.config.bind_addr
		addr_i = self.config.bind_addr_h
        	port = self.config.bind_port
		port_i = self.config.bind_port_h
        	addr_port = (addr, port)
		addr_port_h = (addr_i, port_i)
        	logging.info('Iniciando cliente en %s:%s' % addr_port)
        	trys = 0
		try:
			self.msgudp_sock.bind(addr_port_h)
			self.conn = self.client_sock.connect(addr_port)
		except:
			logging.warn('Se produjo un error de conexion inicial desde %s:%s' % addr_port)
			raise ConnectionException()
		self.__working = True
		logging.info('Conexion creada correctamente')

	def start(self):
		"""
	        Punto de partida de la ejecución del servidor
        	"""
        	# manejo de la señal de finalización de ejecución
        	signal.signal(signal.SIGINT, self.stop)
        	# Configuración del logger
        	logging.basicConfig(
            		filename=self.config.log['filename'],
            		level=getattr(logging, self.config.log['level']),
            		format=self.config.log['format']
        	)
        	self.prepare()
		#Ingresar aca metodo para establecer los parametros si existen o definirlos por el archivo config.
		self.getmsg()	
        	return 0

	def stop(self, sig, frame):
		"""
		Manejo de salida del programa
	        """
		if self.on_work:
	        	self.__working = False
			try:
				self.conn.send(BYE_CMD)
			except:
				pass
            		time.sleep(2)
            		self.client_sock.close()
            		exit(0)

	def validate_msg(info):
		if info[0] != 'OK'
			raise Exception()

	def getmsg(self):
		self.identification_cmd()
		self.msglen_cmd()
		self.givememsg_cmd()
		self.chkmsg_cmd()
		self.bye_cmd()
		print(self.msg)
		
	def identification_cmd(self):
		logging.info('Iniciando identificacion con el servidor')
		try:
			self.conn.send(IDENTIFICATION_CMD + self.config.user)
			data = self.conn.recv(1024)
			info = data.decode('utf-8').strip('\n').split(' ')
			validate_msg(info)
		except:
			logging.warn('Error al identificarse con el servidor : %s' %info[1])
			raise IdentificationException()
		logging.info('Identificacion exitosa con el servidor')

	def msglen_cmd(self):
		logging.info('Iniciando solicitud de longitud de mensaje')
		try:
			self.conn.send(MSGLEN_CMD)
			data = self.conn.recv(1024)
			self.msglen = data.decode('utf-8').strip('\n').split(' ')
			validate_msg(info)
		except:
			logging.warn('Error al intentar solicitar longitud de mensaje : %s' %info[1])
			raise MsglenException()
		logging.info('Longitud establecida con el servidor')

	def givememsg_cmd(self):
		logging.info('Iniciando la recepcion del mensaje')
		try:
			self.conn.send(GIVEMEMSG_CMD + self.config.bind_port_h)
			data = self.msgudp_sock.recvfrom(self.msglen)
			info = data.decode('utf-8').strip('\n').split(' ')
			validate_msg(info)
			self.msgudp_sock.close()
			self.msg = info[1]
		except:
			logging.warn('Error al intentar solicitar el mensaje : %s' %info[1]
			raise GiveMsgException()
		logging.info('Mensaje recibido con exito')

	def chkmsg_cmd(self):
		logging.info('Iniciando la comprobacion del mensaje')
                try:
                        self.conn.send(CHKMSG_CMD + hashlib.md5(self.msg))
                        data = self.conn.recv(1024)
                        info = data.decode('utf-8').strip('\n').split(' ')
                        validate_msg(info)
                except:
                        logging.warn('Error al intentar chequear el mensaje : %s' %info[1]
                        raise ChkMsgException()
                logging.info('Mensaje comprobado con exito')

	def bye_cmd(self):
		logging.info('Iniciando la comprobacion del mensaje')
                try:
			self.stop()
                except:
                        logging.warn('Error al intentar terminar la conexion'
                        raise ByeCmdException()
                logging.info('Conexion terminada con exito')
