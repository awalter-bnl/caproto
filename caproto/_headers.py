# This file auto-generated by `generate_headers.py`.
# Do not modify this file directly.
import ctypes


# constants related to ExtendedMessageHeader
MAX_16BIT = 0xffff
MARKER1 = 0xffff
MARKER2 = 0x0000


class _BaseMessageHeader(ctypes.BigEndianStructure):
    # just to define a nice repr
    def __repr__(self):
        d = [(field, getattr(self, field)) for field, _type in self._fields_]
        formatted_args = ", ".join(["{!s}={!r}".format(k, v) for k, v in d])
        return "{}({})".format(type(self).__name__, formatted_args)


class MessageHeader(_BaseMessageHeader):
    """
    A Structure for the Header of a Channel Access command.

    The specification is documented at:
    http://www.aps.anl.gov/epics/base/R3-16/0-docs/CAproto/index.html#_messages
    """
    _fields_ = [("command", ctypes.c_uint16),
                ("payload_size", ctypes.c_uint16),
                ("data_type", ctypes.c_uint16),
                ("data_count", ctypes.c_uint16),
                ("parameter1", ctypes.c_uint32),
                ("parameter2", ctypes.c_uint32),
               ]


class ExtendedMessageHeader(_BaseMessageHeader):
    """
    A Structure for the Extended Header of a Channel Access command.

    The specification is documented at:
    http://www.aps.anl.gov/epics/base/R3-16/0-docs/CAproto/index.html#_messages
    """
    def __init__(self, command, payload_size, data_type, data_count,
                 parameter1, parameter2):
        super().__init__(command, MARKER1, data_type, MARKER2, parameter1,
                         parameter2, payload_size, data_count)

    _fields_ = [("command", ctypes.c_uint16),
                ("marker1", ctypes.c_uint16),
                ("data_type", ctypes.c_uint16),
                ("marker2", ctypes.c_uint16),
                ("parameter1", ctypes.c_uint32),
                ("parameter2", ctypes.c_uint32),
                ("payload_size", ctypes.c_uint32),
                ("data_count", ctypes.c_uint32),
               ]



def VersionRequestHeader(priority, version):
    """
    Construct a ``MessageHeader`` for a VersionRequest command.

    Exchanges client and server protocol versions and desired circuit priority.
    This is the first message sent when a new TCP (Virtual Circuit) connection
    is established.   Must be sent before any other exchange between client,
    server and repeater.   The communication is not strictly request response,
    but will be perceived as such by the implementation.   When a new TCP
    connection is established by the client, CA_PROTO_VERSION is sent.
    Likewise, the server will accept the connection and send the response form
    back.   Sent over UDP or TCP.

    Parameters
    ----------

    priority : integer
        Virtual circuit priority.

    version : integer
        Minor protocol version number. Only used when sent over TCP.

    """
    return MessageHeader(0, 0, priority, version, 0, 0)


def VersionResponseHeader(version):
    """
    Construct a ``MessageHeader`` for a VersionResponse command.

    Exchanges client and server protocol versions and desired circuit priority.
    This is the first message sent when a new TCP (Virtual Circuit) connection
    is established.   Must be sent before any other exchange between client,
    server and repeater.   The communication is not strictly request response,
    but will be perceived as such by the implementation.   When a new TCP
    connection is established by the client, CA_PROTO_VERSION is sent.
    Likewise, the server will accept the connection and send the response form
    back.   Sent over UDP or TCP.

    Parameters
    ----------

    version : integer
        Minor protocol version number. Only used when sent over TCP.

    """
    return MessageHeader(0, 0, 1, version, 1, 0)


def SearchRequestHeader(payload_size, reply, version, cid):
    """
    Construct a ``MessageHeader`` for a SearchRequest command.

    Searches for a given channel name.   Sent over UDP or TCP.

    Parameters
    ----------

    payload_size : integer
        Padded size of channel name.

    reply : integer
        Search Reply Flag  (8.4.), indicating whether failed search response should
    be returned.

    version : integer
        Client minor protocol version number.

    cid : integer
        Client allocated CID.

    """
    struct_args = (6, payload_size, reply, version, cid, cid)
    # If payload_size or data_count cannot fit into a 16-bit integer, use the
    # extended header.
    return (ExtendedMessageHeader(*struct_args)
            if any((payload_size > 0xffff, version > 0xffff, ))
            else MessageHeader(*struct_args))


def SearchResponseHeader(data_type, sid, cid):
    """
    Construct a ``MessageHeader`` for a SearchResponse command.

    Searches for a given channel name.   Sent over UDP or TCP.

    Parameters
    ----------

    data_type : integer
        TCP Port number of server that responded.

    sid : integer
        Temporary SID, SID - Server ID  (3.2.2.).

    cid : integer
        Channel CID, CID - Client ID  (3.2.1.).

    """
    return MessageHeader(6, 8, data_type, 0, sid, cid)


def NotFoundResponseHeader(reply_flag, version, cid):
    """
    Construct a ``MessageHeader`` for a NotFoundResponse command.

    Indicates that a channel with requested name does not exist.   Sent in
    response to CA_PROTO_SEARCH   (4.6.), but only when its DO_REPLY flag was
    set.   Sent over UDP.

    Parameters
    ----------

    reply_flag : integer
        Same reply flag as in request: always DO_REPLY.

    version : integer
        Client minor protocol version number.

    cid : integer
        CID of the channel.

    """
    return MessageHeader(14, 0, reply_flag, version, cid, cid)


def EchoRequestHeader():
    """
    Construct a ``MessageHeader`` for a EchoRequest command.

    Connection verify used by CA_V43.   Sent over TCP.

    Parameters
    ----------

    """
    return MessageHeader(23, 0, 0, 0, 0, 0)


def EchoResponseHeader():
    """
    Construct a ``MessageHeader`` for a EchoResponse command.

    Connection verify used by CA_V43.   Sent over TCP.

    Parameters
    ----------

    """
    return MessageHeader(23, 0, 0, 0, 0, 0)


def BeaconHeader(version, server_port, beaconid, address):
    """
    Construct a ``MessageHeader`` for a Beacon command.

    Beacon sent by a server when it becomes available.   Beacons are also sent
    out periodically to announce the server is still alive.   Another function
    of beacons is to allow detection of changes in network topology.   Sent
    over UDP.

    Parameters
    ----------

    version : integer
        Minor protocol version.

    server_port : integer
        TCP Port the server is listening on.

    beaconid : integer
        Sequential Beacon ID.

    address : integer
        May contain IP address of the server.

    """
    return MessageHeader(13, 0, version, server_port, beaconid, address)


def RepeaterConfirmResponseHeader(repeater_address):
    """
    Construct a ``MessageHeader`` for a RepeaterConfirmResponse command.

    Confirms successful client registration with repeater.   Sent over UDP.

    Parameters
    ----------

    repeater_address : integer
        Address with which the registration succeeded.

    """
    return MessageHeader(17, 0, 0, 0, 0, repeater_address)


def RepeaterRegisterRequestHeader(client_ip_address):
    """
    Construct a ``MessageHeader`` for a RepeaterRegisterRequest command.

    Requests registration with the repeater.   Repeater will confirm successful
    registration using CA_REPEATER_CONFIRM.   Sent over TCP.

    Parameters
    ----------

    client_ip_address : integer
        IP address on which the client is listening

    """
    return MessageHeader(24, 0, 0, 0, 0, client_ip_address)


def EventAddRequestHeader(data_type, data_count, sid, subscriptionid):
    """
    Construct a ``MessageHeader`` for a EventAddRequest command.

    Creates a subscription on a channel, allowing the client to be notified of
    changes in value.   A request will produce at least one response.   Sent
    over TCP.

    Parameters
    ----------

    data_type : integer
        Desired DBR type of the return value.

    data_count : integer
        Desired number of elements

    sid : integer
        SID of the channel on which to reqister this subscription.   See SID -
    Server ID  (3.2.2.).

    subscriptionid : integer
        Subscription ID identifying this subscription.  See Subscription ID
    (3.2.3.).

    """
    struct_args = (1, 16, data_type, data_count, sid, subscriptionid)
    # If payload_size or data_count cannot fit into a 16-bit integer, use the
    # extended header.
    return (ExtendedMessageHeader(*struct_args)
            if any((16 > 0xffff, data_count > 0xffff, ))
            else MessageHeader(*struct_args))


def EventAddResponseHeader(payload_size, data_type, data_count, status, subscriptionid):
    """
    Construct a ``MessageHeader`` for a EventAddResponse command.

    Creates a subscription on a channel, allowing the client to be notified of
    changes in value.   A request will produce at least one response.   Sent
    over TCP.

    Parameters
    ----------

    payload_size : integer
        Size of the response.

    data_type : integer
        Payload data type.

    data_count : integer
        Payload data count.

    status : integer
        Status code  (13.) (ECA_NORMAL on success).

    subscriptionid : integer
        Subscription ID

    """
    struct_args = (1, payload_size, data_type, data_count, status, subscriptionid)
    # If payload_size or data_count cannot fit into a 16-bit integer, use the
    # extended header.
    return (ExtendedMessageHeader(*struct_args)
            if any((payload_size > 0xffff, data_count > 0xffff, ))
            else MessageHeader(*struct_args))


def EventCancelRequestHeader(data_type, data_count, sid, subscriptionid):
    """
    Construct a ``MessageHeader`` for a EventCancelRequest command.

    Clears event subscription.   This message will stop event updates for
    specified channel.   Sent over TCP.

    Parameters
    ----------

    data_type : integer
        Same value as in corresponding CA_PROTO_EVENT_ADD  (6.1.).

    data_count : integer
        Same value as in corresponding CA_PROTO_EVENT_ADD  (6.1.).

    sid : integer
        Same value as in corresponding CA_PROTO_EVENT_ADD  (6.1.).

    subscriptionid : integer
        Same value as in corresponding CA_PROTO_EVENT_ADD  (6.1.).

    """
    struct_args = (2, 0, data_type, data_count, sid, subscriptionid)
    # If payload_size or data_count cannot fit into a 16-bit integer, use the
    # extended header.
    return (ExtendedMessageHeader(*struct_args)
            if any((data_count > 0xffff, ))
            else MessageHeader(*struct_args))


def EventCancelResponseHeader(data_type, data_count, sid, subscriptionid):
    """
    Construct a ``MessageHeader`` for a EventCancelResponse command.

    Clears event subscription.   This message will stop event updates for
    specified channel.   Sent over TCP.

    Parameters
    ----------

    data_type : integer
        Same value as CA_PROTO_EVENT_ADD request.

    data_count : integer
        Same value as CA_PROTO_EVENT_ADD request.

    sid : integer
        Same value as CA_PROTO_EVENT_ADD request.

    subscriptionid : integer
        Same value as CA_PROTO_EVENT_ADD request.

    """
    struct_args = (1, 0, data_type, data_count, sid, subscriptionid)
    # If payload_size or data_count cannot fit into a 16-bit integer, use the
    # extended header.
    return (ExtendedMessageHeader(*struct_args)
            if any((data_count > 0xffff, ))
            else MessageHeader(*struct_args))


def ReadRequestHeader(data_type, data_count, sid, ioid):
    """
    Construct a ``MessageHeader`` for a ReadRequest command.

    Read value of a channel. Sent over TCP.   Deprecated since protocol version
    3.13.

    Parameters
    ----------

    data_type : integer
        Desired type of the return value.

    data_count : integer
        Desired number of elements to read.

    sid : integer
        SID of the channel to read.

    ioid : integer
        IOID of this operation.

    """
    struct_args = (3, 0, data_type, data_count, sid, ioid)
    # If payload_size or data_count cannot fit into a 16-bit integer, use the
    # extended header.
    return (ExtendedMessageHeader(*struct_args)
            if any((data_count > 0xffff, ))
            else MessageHeader(*struct_args))


def ReadResponseHeader(payload_size, data_type, data_count, sid, ioid):
    """
    Construct a ``MessageHeader`` for a ReadResponse command.

    Read value of a channel. Sent over TCP.   Deprecated since protocol version
    3.13.

    Parameters
    ----------

    payload_size : integer
        Size of DBR formatted data in payload.

    data_type : integer
        Payload format.

    data_count : integer
        Payload element count.

    sid : integer
        SID of the channel.

    ioid : integer
        IOID of this operation.

    """
    struct_args = (3, payload_size, data_type, data_count, sid, ioid)
    # If payload_size or data_count cannot fit into a 16-bit integer, use the
    # extended header.
    return (ExtendedMessageHeader(*struct_args)
            if any((payload_size > 0xffff, data_count > 0xffff, ))
            else MessageHeader(*struct_args))


def WriteRequestHeader(payload_size, data_type, data_count, sid, ioid):
    """
    Construct a ``MessageHeader`` for a WriteRequest command.

    Writes new channel value.   Sent over TCP.

    Parameters
    ----------

    payload_size : integer
        Size of padded payload

    data_type : integer
        Format of payload

    data_count : integer
        Number of elements in payload

    sid : integer
        Server channel ID

    ioid : integer
        Request ID

    """
    struct_args = (4, payload_size, data_type, data_count, sid, ioid)
    # If payload_size or data_count cannot fit into a 16-bit integer, use the
    # extended header.
    return (ExtendedMessageHeader(*struct_args)
            if any((payload_size > 0xffff, data_count > 0xffff, ))
            else MessageHeader(*struct_args))


def EventsOffRequestHeader():
    """
    Construct a ``MessageHeader`` for a EventsOffRequest command.

    Disables a server from sending any subscription updates over this virtual
    circuit.   Sent over TCP.   This mechanism is used by clients with slow CPU
    to prevent congestion when they are unable to handle all updates recived.
    Effective automated handling of flow control is beyond the scope of this
    document.

    Parameters
    ----------

    """
    return MessageHeader(8, 0, 0, 0, 0, 0)


def EventsOnRequestHeader():
    """
    Construct a ``MessageHeader`` for a EventsOnRequest command.

    Enables the server to resume sending subscription updates for this virtual
    circuit.   Sent over TCP.   This mechanism is used by clients with slow CPU
    to prevent congestion when they are unable to handle all updates recived.
    Effective automated handling of flow control is beyond the scope of this
    document.

    Parameters
    ----------

    """
    return MessageHeader(9, 0, 0, 0, 0, 0)


def ReadSyncRequestHeader():
    """
    Construct a ``MessageHeader`` for a ReadSyncRequest command.

    Deprecated since protocol version 3.13.

    Parameters
    ----------

    """
    return MessageHeader(10, 0, 0, 0, 0, 0)


def ErrorResponseHeader(payload_size, cid, status):
    """
    Construct a ``MessageHeader`` for a ErrorResponse command.

    Sends error message and code.   This message is only sent from server to
    client in response to any request that fails and does not include error
    code in response.   This applies to all asynchronous commands.   Error
    message will contain a copy of original request and textual description of
    the error.   Sent over UDP.

    Parameters
    ----------

    payload_size : integer
        Size of the request header that triggered the error plus size of the error
    message.

    cid : integer
        CID of the channel for which request failed, CID - Client ID  (3.2.1.).

    status : integer
        Error status code  (13.).

    """
    struct_args = (11, payload_size, 0, 0, cid, status)
    # If payload_size or data_count cannot fit into a 16-bit integer, use the
    # extended header.
    return (ExtendedMessageHeader(*struct_args)
            if any((payload_size > 0xffff, ))
            else MessageHeader(*struct_args))


def ClearChannelRequestHeader(sid, cid):
    """
    Construct a ``MessageHeader`` for a ClearChannelRequest command.

    Clears a channel.   This command will cause server to release the
    associated channel resources and no longer accept any requests for this
    SID/CID.

    Parameters
    ----------

    sid : integer
        SID of channel to clear.

    cid : integer
        CID of channel to clear.

    """
    return MessageHeader(12, 0, 0, 0, sid, cid)


def ClearChannelResponseHeader(sid, cid):
    """
    Construct a ``MessageHeader`` for a ClearChannelResponse command.

    Clears a channel.   This command will cause server to release the
    associated channel resources and no longer accept any requests for this
    SID/CID.

    Parameters
    ----------

    sid : integer
        SID of cleared channel.

    cid : integer
        CID of cleared channel.

    """
    return MessageHeader(12, 0, 0, 0, sid, cid)


def ReadNotifyRequestHeader(data_type, data_count, sid, ioid):
    """
    Construct a ``MessageHeader`` for a ReadNotifyRequest command.

    Read value of a channel. Sent over TCP.

    Parameters
    ----------

    data_type : integer
        Desired type of the return value.

    data_count : integer
        Desired number of elements to read.

    sid : integer
        SID of the channel to read.

    ioid : integer
        IOID of this operation.

    """
    struct_args = (15, 0, data_type, data_count, sid, ioid)
    # If payload_size or data_count cannot fit into a 16-bit integer, use the
    # extended header.
    return (ExtendedMessageHeader(*struct_args)
            if any((data_count > 0xffff, ))
            else MessageHeader(*struct_args))


def ReadNotifyResponseHeader(payload_size, data_type, data_count, sid, ioid):
    """
    Construct a ``MessageHeader`` for a ReadNotifyResponse command.

    Read value of a channel. Sent over TCP.

    Parameters
    ----------

    payload_size : integer
        Size of DBR formatted data in payload.

    data_type : integer
        Payload format.

    data_count : integer
        Payload element count.

    sid : integer
        SID of the channel.

    ioid : integer
        IOID of this operation.

    """
    struct_args = (15, payload_size, data_type, data_count, sid, ioid)
    # If payload_size or data_count cannot fit into a 16-bit integer, use the
    # extended header.
    return (ExtendedMessageHeader(*struct_args)
            if any((payload_size > 0xffff, data_count > 0xffff, ))
            else MessageHeader(*struct_args))


def CreateChanRequestHeader(payload_size, cid, client_version):
    """
    Construct a ``MessageHeader`` for a CreateChanRequest command.

    Requests creation of channel.   Server will allocate required resources and
    return initialized SID.   Sent over TCP.

    Parameters
    ----------

    payload_size : integer
        Padded length of channel name.

    cid : integer
        CID of the channel to create.

    client_version : integer
        Client minor protocol version.

    """
    struct_args = (18, payload_size, 0, 0, cid, client_version)
    # If payload_size or data_count cannot fit into a 16-bit integer, use the
    # extended header.
    return (ExtendedMessageHeader(*struct_args)
            if any((payload_size > 0xffff, ))
            else MessageHeader(*struct_args))


def CreateChanResponseHeader(data_type, data_count, cid, sid):
    """
    Construct a ``MessageHeader`` for a CreateChanResponse command.

    Requests creation of channel.   Server will allocate required resources and
    return initialized SID.   Sent over TCP.

    Parameters
    ----------

    data_type : integer
        Native channel data type

    data_count : integer
        Native channel data count

    cid : integer
        Channel client ID

    sid : integer
        Channel server ID

    """
    struct_args = (18, 0, data_type, data_count, cid, sid)
    # If payload_size or data_count cannot fit into a 16-bit integer, use the
    # extended header.
    return (ExtendedMessageHeader(*struct_args)
            if any((data_count > 0xffff, ))
            else MessageHeader(*struct_args))


def WriteNotifyRequestHeader(payload_size, data_type, data_count, sid, ioid):
    """
    Construct a ``MessageHeader`` for a WriteNotifyRequest command.

    Writes new channel value.   Sent over TCP.

    Parameters
    ----------

    payload_size : integer
        Size of padded payload

    data_type : integer
        Format of payload

    data_count : integer
        Number of elements in payload

    sid : integer
        Server channel ID

    ioid : integer
        Request ID

    """
    struct_args = (19, payload_size, data_type, data_count, sid, ioid)
    # If payload_size or data_count cannot fit into a 16-bit integer, use the
    # extended header.
    return (ExtendedMessageHeader(*struct_args)
            if any((payload_size > 0xffff, data_count > 0xffff, ))
            else MessageHeader(*struct_args))


def WriteNotifyResponseHeader(data_type, data_count, status, ioid):
    """
    Construct a ``MessageHeader`` for a WriteNotifyResponse command.

    Writes new channel value.   Sent over TCP.

    Parameters
    ----------

    data_type : integer
        Format of data written

    data_count : integer
        Number of elements written

    status : integer
        Status of write success

    ioid : integer
        Request ID

    """
    struct_args = (19, 0, data_type, data_count, status, ioid)
    # If payload_size or data_count cannot fit into a 16-bit integer, use the
    # extended header.
    return (ExtendedMessageHeader(*struct_args)
            if any((data_count > 0xffff, ))
            else MessageHeader(*struct_args))


def ClientNameRequestHeader(payload_size):
    """
    Construct a ``MessageHeader`` for a ClientNameRequest command.

    Sends local username to virtual circuit peer.  This name identifies the
    user and affects access rights.

    Parameters
    ----------

    payload_size : integer
        Length of string in payload

    """
    struct_args = (20, payload_size, 0, 0, 0, 0)
    # If payload_size or data_count cannot fit into a 16-bit integer, use the
    # extended header.
    return (ExtendedMessageHeader(*struct_args)
            if any((payload_size > 0xffff, ))
            else MessageHeader(*struct_args))


def HostNameRequestHeader(payload_size):
    """
    Construct a ``MessageHeader`` for a HostNameRequest command.

    Sends local host name to virtual circuit peer.   This name will affect
    access rights.   Sent over TCP.

    Parameters
    ----------

    payload_size : integer
        Length of host name string.

    """
    struct_args = (21, payload_size, 0, 0, 0, 0)
    # If payload_size or data_count cannot fit into a 16-bit integer, use the
    # extended header.
    return (ExtendedMessageHeader(*struct_args)
            if any((payload_size > 0xffff, ))
            else MessageHeader(*struct_args))


def AccessRightsResponseHeader(cid, access_rights):
    """
    Construct a ``MessageHeader`` for a AccessRightsResponse command.

    Notifies of access rights for a channel.   This value is determined based
    on host and client name and may change during runtime.   Client cannot
    change access rights nor can it explicitly query its value, so last
    received value must be stored.

    Parameters
    ----------

    cid : integer
        Channel affected by change.

    access_rights : integer
        Access rights  (8.5.) for given channel.

    """
    return MessageHeader(22, 0, 0, 0, cid, access_rights)


def CreateChFailResponseHeader(cid):
    """
    Construct a ``MessageHeader`` for a CreateChFailResponse command.

    Reports that channel creation failed.   This response is sent to when
    channel creation in CA_PROTO_CREATE_CHAN fails.

    Parameters
    ----------

    cid : integer
        Client channel ID

    """
    return MessageHeader(26, 0, 0, 0, cid, 0)


def ServerDisconnResponseHeader(cid):
    """
    Construct a ``MessageHeader`` for a ServerDisconnResponse command.

    Notifies the client that server has disconnected the channel.   This may be
    since the channel has been destroyed on server.   Sent over TCP.

    Parameters
    ----------

    cid : integer
        CID that was provided during CA_PROTO_CREATE_CHAN

    """
    return MessageHeader(27, 0, 0, 0, cid, 0)


# This file auto-generated by `generate_headers.py`.
# Do not modify this file directly.
# (end of auto-generated code)