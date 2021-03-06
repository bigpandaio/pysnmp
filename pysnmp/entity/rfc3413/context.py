#
# This file is part of pysnmp software.
#
# Copyright (c) 2005-2019, Ilya Etingof <etingof@gmail.com>
# License: http://snmplabs.com/pysnmp/license.html
#
from pyasn1.compat.octets import null
from pyasn1.type import univ

from pysnmp import debug
from pysnmp import error


class SnmpContext(object):
    def __init__(self, snmpEngine, contextEngineId=None):
        mibBuilder = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder

        snmpEngineId, = mibBuilder.importSymbols('__SNMP-FRAMEWORK-MIB', 'snmpEngineID')

        if contextEngineId is None:
            # Default to local snmpEngineId
            self.contextEngineId = snmpEngineId.syntax

        else:
            self.contextEngineId = snmpEngineId.syntax.clone(contextEngineId)

        debug.logger & debug.FLAG_INS and debug.logger(
            'SnmpContext: contextEngineId %r' % (self.contextEngineId,))

        self.contextNames = {
            null: snmpEngine.msgAndPduDsp.mibInstrumController  # Default name
        }

    def registerContextName(self, contextName, mibInstrum=None):
        contextName = univ.OctetString(contextName).asOctets()
        if contextName in self.contextNames:
            raise error.PySnmpError(
                'Duplicate contextName %s' % contextName)

        debug.logger & debug.FLAG_INS and debug.logger(
            'registerContextName: registered contextName %r, mibInstrum %r' % (contextName, mibInstrum))

        if mibInstrum is None:
            self.contextNames[contextName] = self.contextNames[null]

        else:
            self.contextNames[contextName] = mibInstrum

    def unregisterContextName(self, contextName):
        contextName = univ.OctetString(contextName).asOctets()

        if contextName in self.contextNames:
            debug.logger & debug.FLAG_INS and debug.logger(
                'unregisterContextName: unregistered contextName %r' % contextName)

            del self.contextNames[contextName]

    def getMibInstrum(self, contextName=null):
        contextName = univ.OctetString(contextName).asOctets()
        if contextName not in self.contextNames:
            debug.logger & debug.FLAG_INS and debug.logger('getMibInstrum: contextName %r not registered' % contextName)

            raise error.PySnmpError('Missing contextName %s' % contextName)

        else:
            debug.logger & debug.FLAG_INS and debug.logger(
                'getMibInstrum: contextName %r, mibInstum %r' % (contextName, self.contextNames[contextName]))

            return self.contextNames[contextName]
