import os
import unittest
from argparse import Namespace
from port.port import main as port_main
from port.cslang_error import CSlangError


def get_test_data_path(filename):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, filename)


class TestArgs(unittest.TestCase):
    def test_exception_on_both_c_and_s(self):
        with self.assertRaises(CSlangError) as cm:
            ast = port_main(
                Namespace(
                    mode="parse",
                    cslang_file="test/bad.cslang",
                    check=True,
                    string="""
event read {filedesc: Numeric@0};
bad <- 4;
NOT read({}) -> read({filedesc: ->bad});
""",
                )
            )

    def test_skip(self):
        port_main(
            Namespace(mode="build", cslang_path=get_test_data_path("open.cslang"))
        )
        automaton, datawords_after, _ = port_main(
            Namespace(
                mode="run",
                format="strace",
                skip=2,
                strace_path=get_test_data_path("openclose.strace"),
                syscall_definitions=get_test_data_path(
                    "../port/syscall_definitions.pickle"
                ),
                automaton_path=get_test_data_path("open.auto"),
            )
        )
        assert len(datawords_after) == 1
