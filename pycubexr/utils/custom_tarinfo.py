import struct
import tarfile
import warnings

BLOCKSIZE = 512
NUL = b"\0"


def nti(s):
    """Convert a number field to a python number.
    """
    # Copyright (C) 2002 Lars Gustaebel <lars@gustaebel.de>
    # All rights reserved.
    #
    # Permission  is  hereby granted,  free  of charge,  to  any person
    # obtaining a  copy of  this software  and associated documentation
    # files  (the  "Software"),  to   deal  in  the  Software   without
    # restriction,  including  without limitation  the  rights to  use,
    # copy, modify, merge, publish, distribute, sublicense, and/or sell
    # copies  of  the  Software,  and to  permit  persons  to  whom the
    # Software  is  furnished  to  do  so,  subject  to  the  following
    # conditions:
    #
    # The above copyright  notice and this  permission notice shall  be
    # included in all copies or substantial portions of the Software.
    #
    # THE SOFTWARE IS PROVIDED "AS  IS", WITHOUT WARRANTY OF ANY  KIND,
    # EXPRESS OR IMPLIED, INCLUDING  BUT NOT LIMITED TO  THE WARRANTIES
    # OF  MERCHANTABILITY,  FITNESS   FOR  A  PARTICULAR   PURPOSE  AND
    # NONINFRINGEMENT.  IN  NO  EVENT SHALL  THE  AUTHORS  OR COPYRIGHT
    # HOLDERS  BE LIABLE  FOR ANY  CLAIM, DAMAGES  OR OTHER  LIABILITY,
    # WHETHER  IN AN  ACTION OF  CONTRACT, TORT  OR OTHERWISE,  ARISING
    # FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    # OTHER DEALINGS IN THE SOFTWARE.

    # There are two possible encodings for a number field, see
    # itn() below.
    if s[0] in (0o200, 0o377):
        n = 0
        for i in range(len(s) - 1):
            n <<= 8
            n += s[i + 1]
        if s[0] == 0o377:
            n = -(256 ** (len(s) - 1) - n)
    else:
        try:
            p = s.find(b"\0")
            if p != -1:
                s = s[:p]
            s = s.decode("ascii", "strict")
            n = int(s.strip() or "0", 8)
        except ValueError:
            raise ValueError("invalid tar header")
    return n


class TarInfoWithoutCheck(tarfile.TarInfo):
    checksum_warning = "Detected invalid checksum in CUBE file header. Proceeding without checking checksums. " \
                       "If CubeWriter 4.8 was used to create this file, you can ignore this warning."

    @classmethod
    def frombuf(cls, buf, encoding, errors):
        if len(buf) == 0:
            super(TarInfoWithoutCheck, cls).frombuf(buf, encoding, errors)
        if len(buf) != BLOCKSIZE:
            super(TarInfoWithoutCheck, cls).frombuf(buf, encoding, errors)
        if buf.count(tarfile.NUL) == BLOCKSIZE:
            super(TarInfoWithoutCheck, cls).frombuf(buf, encoding, errors)

        chksum = nti(buf[148:156])
        unsigned_chksum = 256 + sum(struct.unpack_from("148B8x356B", buf))
        signed_chksum = 256 + sum(struct.unpack_from("148b8x356b", buf))
        calculated_checksums = unsigned_chksum, signed_chksum
        if chksum not in calculated_checksums:
            warnings.warn(cls.checksum_warning)
        buf = buf[:148] + bytes("%07o\0" % unsigned_chksum, "ascii") + buf[156:]

        return super(TarInfoWithoutCheck, cls).frombuf(buf, encoding, errors)
