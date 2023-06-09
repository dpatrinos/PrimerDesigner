import pytest
import sys
import os

sys.path.append('src/primerdesigner')
from primerdesigner import fromCoordinates
from primerdesigner import fromSJDataset

def test_fromCoordinates_plus(tmpdir):
    fromCoordinates("1", "+", 163310, 163645, 150, 150, tmpdir)

    assert os.path.exists(os.path.join(tmpdir, "chr1_163310-163645.fasta"))
    assert os.path.getsize(os.path.join(tmpdir, "chr1_163310-163645.fasta")) > 0
    with open(os.path.join(tmpdir, "chr1_163310-163645.fasta"), "r") as f:
        with open(os.path.abspath(os.path.join("tests", "test_fromCoordinates_plus.fasta")), "r") as f2:
            assert f.read() == f2.read()

def test_fromCoordinates_minus(tmpdir):
    fromCoordinates("5", "-", 131673575, 131673600, 150, 150, tmpdir)

    assert os.path.exists(os.path.join(tmpdir, "chr5_131673575-131673600.fasta"))
    assert os.path.getsize(os.path.join(tmpdir, "chr5_131673575-131673600.fasta")) > 0
    with open(os.path.join(tmpdir, "chr5_131673575-131673600.fasta"), "r") as f:
        with open(os.path.abspath(os.path.join("tests", "test_fromCoordinates_minus.fasta")), "r") as f2:
            assert f.read() == f2.read()

def test_fromSJDataset(tmpdir):
    fromSJDataset(1, "+", 150, 150, "tests/test_fromSJDataset.csv", tmpdir)

    assert os.path.exists(os.path.join(tmpdir, "chr1_163310-163645.fasta"))
    assert os.path.getsize(os.path.join(tmpdir, "chr1_163310-163645.fasta")) > 0
    with open(os.path.join(tmpdir, "chr1_163310-163645.fasta"), "r") as f:
        with open(os.path.abspath(os.path.join("tests", "test_fromCoordinates_plus.fasta")), "r") as f2:
            assert f.read() == f2.read()