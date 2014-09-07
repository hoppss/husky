"""
  'Database' of messages
"""

import struct


def lookupTopicType( topic ):
    tab = { 
            '/hello': ("std_msgs/String", '992ce8a1687cec8c8bd883ec73ca41d1', parseString, packString),
            '/imu/data': ("std_msgs/Imu", "6a62c6daae103f4ff57a132d6f95cec2", parseImu),
            '/imu/mag': ("geometry_msgs/Vector3Stamped", "7b324c7325e683bf02a9b14b01090ec7", parseVector3),
            '/imu/rpy': ("geometry_msgs/Vector3Stamped", "7b324c7325e683bf02a9b14b01090ec7", parseNone),
            '/imu/temperature': ("std_msgs/Float32", "73fcbf46b49191e672908e50842a83d4", parseNone),
            '/husky/data/encoders': ("clearpath_base/Encoders", '2ea748832c2014369ffabd316d5aad8c', parseEncoders),
            '/husky/data/power_status': ('clearpath_base/PowerStatus', 'f246c359530c58415aee4fe89d1aca04', parsePower),
            '/husky/data/safety_status': ('clearpath_base/SafetyStatus', 'cf78d6042b92d64ebda55641e06d66fa', parseNone), # TODO
            '/husky/data/system_status': ('clearpath_base/SystemStatus', 'b24850c808eb727058fff35ba598006f', parseNone), # TODO
            '/husky/cmd_vel' : ('geometry_msgs/Twist', '9f195f881246fdfa2798d1d3eebca84a', parseNone, packCmdVel),
            '/joy': ('sensor_msgs/Joy', '5a9ea5f83505693b71e785041e67a8bb', parseJoy),
          }       
    return tab[topic]



def parseNone( data ):
    "dummy parser"
    return len(data)

def parseString( data ):
    n = struct.unpack("I", data[:4])[0]
    return data[4:4+n]

def packString( s ):
    return struct.pack("I", len(s)) + s


def packCmdVel( speed, angularSpeed ):
    return struct.pack("dddddd", speed,0,0, 0,0,angularSpeed)


def parseImu( data ):
    seq, stamp, stampNsec, frameIdLen = struct.unpack("IIII", data[:16])
#    print seq, stamp, stampNsec, frameIdLen
#    print data[16:16+frameIdLen]
    data = data[16+frameIdLen:]
    orientation = struct.unpack("dddd", data[:4*8])
    data = data[4*8+9*8:] # skip covariance matrix
    angularVelocity = struct.unpack("ddd", data[:3*8])
    data = data[3*8+9*8:] # skip velocity covariance
    linearAcceleration = struct.unpack("ddd", data[:3*8])
    data = data[3*8+9*8:] # skip velocity covariance
    assert len(data) == 0, len(data)
    return orientation

def parseVector3( data ):
    seq, stamp, stampNsec, frameIdLen = struct.unpack("IIII", data[:16])
    data = data[16+frameIdLen:]
    return struct.unpack("ddd", data)


def parseEncoders( data ):
    seq, stamp, stampNsec, frameIdLen = struct.unpack("IIII", data[:16])
#    print seq, stamp, stampNsec, frameIdLen
    assert frameIdLen == 0, frameIdLen
    data = data[16+frameIdLen:]
    arrLen, travelL,speedL, travelR,speedR = struct.unpack("=Idddd", data)
    assert arrLen==2, arrLen
    return stamp+stampNsec/1000000000., (travelL,speedL), (travelR,speedR)


def parsePower( data ):
    seq, stamp, stampNsec, frameIdLen = struct.unpack("IIII", data[:16])
#    print seq, stamp, stampNsec, frameIdLen
    assert frameIdLen == 0, frameIdLen
    data = data[16+frameIdLen:]
    arrLen, charge, capacity, present, inUse, description = struct.unpack("=Ifh??B", data)
    assert arrLen==1, arrLen
    return charge

def parseJoy( data ):
    seq, stamp, stampNsec, frameIdLen = struct.unpack("IIII", data[:16])
#    print seq, stamp, stampNsec, frameIdLen
    assert frameIdLen == 0, frameIdLen
    data = data[16+frameIdLen:]
    # float32[] axes          # the axes measurements from a joystick
    # int32[] buttons         # the buttons measurements from a joystick  
    numAxes = struct.unpack("I", data[:4])[0]
    axes = struct.unpack("f"*numAxes, data[4:4+4*numAxes])
    data = data[4+4*numAxes:]
    numButtons = struct.unpack("I", data[:4])[0]
    buttons = struct.unpack("I"*numButtons, data[4:])
    return axes, buttons

def parseSafety( data ):
    seq, stamp, stampNsec, frameIdLen = struct.unpack("IIII", data[:16])
#    print seq, stamp, stampNsec, frameIdLen
    data = data[16+frameIdLen:]
    # uint16 flags  ... not very descriptive
    # bool estop
    return struct.unpack("H?", data)

#-------------------------------------------------------------------
# vim: expandtab sw=4 ts=4

