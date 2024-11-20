class PublicKeyRequest:
  def __init__(self, request_for, requested_by):
    self.request_for = request_for
    self.requested_by = requested_by
  
  def to_msg(self):
    return {
      'request_for': self.request_for,
      'requested_by': self.requested_by
    }
    
class PublicKeyResponse:
  def __init__(self, type="error", value=None, message=None):
    self.type = type
    self.value = value
    self.message = message
  
  def to_msg(self):
    return {
      'type': self.type,
      'value': self.value,
      'message': self.message
    }

def read_all(client, buf_size=1024):
  data = b''
  while True:
    packet = client.recv(buf_size)
    data += packet
    if len(packet) < buf_size:
      break
  return data