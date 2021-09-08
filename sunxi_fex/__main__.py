#!/usr/bin/env python3

import argparse
import configparser
import sys
from io import StringIO
from abc import ABC, abstractmethod

from kaitaistruct import KaitaiStruct
from plumbum import cli

from collections import OrderedDict

from . import SunxiFex

from pathlib import Path

indent = "\t"
opener = " {"
closer = "}"
terminator = ";"
assignment = " = "
rootNode = "/"
closerWithTerminator = closer + terminator

Type = SunxiFex.Level2Node.Level3Node.Type


def ksReprGen(struct):
	return ((str(k), getattr(struct, k)) for k in dir(struct) if k[0] != "_" and not hasattr(KaitaiStruct, k) and not isinstance(getattr(struct, k), type))


class Printer:
	@abstractmethod
	def __call__(this, parsed):
		raise NotImplementedError

	EXT = None


class FdtPrinter(Printer):
	EXT = "dts"

	@classmethod
	def arrayRepr(cls, v):
		return "<" + ", ".join(hex(el) for el in v) + ">"

	@classmethod
	def u32Repr(cls, v):
		return cls.arrayRepr((v,))

	@classmethod
	def gpioU32Repr(cls, v):
		res = [opener]
		if v.name:
			res.append(indent * 4 + "name" + cls.fdtReprByType(v.name) + terminator)
		for k, v in ksReprGen(v.descriptor):
			res.append(indent * 4 + k + cls.fdtReprByType(v) + terminator)
		res.append(indent * 3 + closer)
		return "\n".join(res)

	reprTypeMapper = {
		str: lambda cls, v: assignment + '"' + v.replace('"', '\\"') + '"',
		int: lambda cls, v: assignment + cls.u32Repr(v),
		list: lambda cls, v: assignment + cls.arrayRepr(v)
	}

	@classmethod
	def fdtReprByType(cls, v):
		return cls.reprTypeMapper[type(v)](cls, v)

	typPrinterMapping = {
		Type.string: reprTypeMapper[str],
		Type.u32: reprTypeMapper[int],
		Type.empty: lambda cls, v: "",
		Type.gpio_u32: lambda cls, v: cls.gpioU32Repr(v),
	}

	@classmethod
	def fdtReprByTypeEnum(cls, typ, v):
		return cls.typPrinterMapping[typ](cls, v)

	@classmethod
	def _generate(cls, parsed):
		yield "/dts-v1/;"
		yield ""
		yield rootNode + opener

		yield indent + "soc@<addr>" + opener
		for l2el in parsed.level_2:
			yield indent * 2 + l2el.key + opener
			for l3el in l2el.level_3:
				# yield "#" + indent * 3 + l3el.key, l3el.type
				yield indent * 3 + l3el.key + cls.fdtReprByTypeEnum(l3el.type, l3el.value) + terminator
			yield indent * 2 + closer

		yield indent + closerWithTerminator
		yield closerWithTerminator

	@classmethod
	def __call__(cls, parsed):
		return "\n".join(cls._generate(parsed))


class FexPrinter(Printer):
	EXT = "fex"

	@classmethod
	def filterGpioValue(cls, v):
		if v == 0xFFFFFFFF:
			return "default"
		else:
			return str(v)

	@classmethod
	def gpioU32Repr(cls, v):
		d = v.descriptor

		if v.name:
			name = v.name
		else:
			pn = str(d.idx)
			if d.port != 0xFFFF:
				pLetter = chr(ord("A") + d.port - 1)
				pn = "0" * (2 - len(pn)) + pn
				name = "P" + pLetter + pn
			else:
				name = "power" + pn

		return "port:" + name + "<" + cls.filterGpioValue(d.muxsel) + "><" + cls.filterGpioValue(d.pull) + "><" + cls.filterGpioValue(d.drive) + "><" + cls.filterGpioValue(d.data) + ">"

	typPrinterMapping = {
		Type.string: lambda cls, v: '"' + v.replace('"', '\\"') + '"',
		Type.empty: lambda cls, v: "",
		Type.gpio_u32: lambda cls, v: cls.gpioU32Repr(v),
	}

	@classmethod
	def fdtReprByTypeEnum(cls, typ, v):
		return cls.typPrinterMapping.get(typ, lambda cls, v: v)(cls, v)

	@classmethod
	def __call__(cls, parsed):
		ini = configparser.ConfigParser()

		for l2el in parsed.level_2:
			l2ini = ini[l2el.key] = OrderedDict((l3el.key, cls.fdtReprByTypeEnum(l3el.type, l3el.value)) for l3el in l2el.level_3)
		with StringIO() as f:
			ini.write(f)
			return f.getvalue()


defaultFileName = "./soc-cfg"

printers = OrderedDict((
	("fex", FexPrinter),
	("fdt", FdtPrinter)
))

class TransformerzPrinter(Printer):
	TRANSFORMER = None

	@classmethod
	def gpioU32Repr(cls, v):
		return OrderedDict(ksReprGen(v.descriptor))

	@classmethod
	def fdtReprByTypeEnum(cls, typ, v):
		if typ == Type.gpio_u32:
			return cls.gpioU32Repr(v)
		elif typ == Type.empty:
			return True
		return v

	@classmethod
	def __call__(cls, parsed):
		dic = OrderedDict()

		for l2el in parsed.level_2:
			l2ini = dic[l2el.key] = {l3el.key: cls.fdtReprByTypeEnum(l3el.type, l3el.value) for l3el in l2el.level_3}

		return cls.TRANSFORMER.unprocess(dic)


def transformerzPrinterFactory(transformer: "transformerz.core.Transformer") -> TransformerzPrinter:
	class ThisPrinter(TransformerzPrinter):
		TRANSFORMER = transformer

		@property
		def EXT(self):
			return self.TRANSFORMER.fileExtension

	return ThisPrinter


try:
	from transformerz.serialization.json import jsonFancySerializer
except ImportError:
	pass
else:
	printers["json"] = transformerzPrinterFactory(jsonFancySerializer)

try:
	from transformerz.serialization.yaml import yamlSerializer
except ImportError:
	pass
else:
	printers["yaml"] = transformerzPrinterFactory(yamlSerializer)

try:
	from transformerz.serialization.pon import ponSerializer
except ImportError:
	pass
else:
	class PonSerializer(transformerzPrinterFactory(ponSerializer)):
		EXT = "pon"

	printers["pon"] = PonSerializer

try:
	from transformerz.serialization.cbor import cborSerializer
except ImportError:
	pass
else:
	printers["cbor"] = transformerzPrinterFactory(cborSerializer)

try:
	from transformerz.serialization.msgpack import msgpackSerializer
except ImportError:
	pass
else:
	printers["msgpack"] = transformerzPrinterFactory(msgpackSerializer)

try:
	from transformerz.serialization.ubjson import ubjsonSerializer
except ImportError:
	pass
else:
	printers["ubjson"] = transformerzPrinterFactory(ubjsonSerializer)


class CLI(cli.Application):
	"""fex reserializer"""

	printerIds = cli.SwitchAttr("-O", cli.Set(*printers.keys(), csv=True), default="fex", help="Type of output")

	def main(self, *files: cli.ExistingFile):

		for pI in self.printerIds:
			printerCtor = printers[pI]
			printer = printerCtor()

			if not files:
				print("Assumming that the data is in", defaultFileName, file=sys.stderr)
				files = (defaultFileName,)

			for f in files:
				f = Path(f)
				parsed = SunxiFex.from_file(f)

				stem = f.name if f.suffix.lower() != ".bin" else f.stem

				ofn = f.parent / (stem + "." + printer.EXT)
				r = printer(parsed)

				if isinstance(r, str):
					ofn.write_text(r)
				else:
					ofn.write_bytes(r)


if __name__ == "__main__":
	CLI.run()
