import os
import unittest
from argparse import Namespace
from port.port import main as port_main
from port.cslang_error import CSlangError


def get_test_data_path(filename):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, filename)


class TestUnusualFiletype(unittest.TestCase):
    def test_stat_blk(self):
        automaton, cb = port_main(
            Namespace(mode="build", cslang_path=get_test_data_path("stat_blk.cslang"))
        )
        automaton, datawords_after, _ = port_main(
            Namespace(
                mode="run",
                format="strace",
                strace_path=get_test_data_path("stat_blk.strace"),
                syscall_definitions=get_test_data_path(
                    "../port/syscall_definitions.pickle"
                ),
                automaton_path=get_test_data_path("stat_blk.auto"),
            )
        )

        assert automaton
        assert len(automaton.states) == 2
        assert automaton.states[1].name == "stat"
