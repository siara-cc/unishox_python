"""
 * Copyright (C) 2020 Siara Logics (cc)
 *
 * Licensed under the Apache License, Version 2.0 (the "License")
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * @author Arundale Ramanathan
 *
"""
class Unishox2:
  USX_HCODES_DFLT = bytearray([0x00, 0x40, 0xE0, 0x80, 0xC0])
  USX_HCODE_LENS_DFLT = bytearray([2, 2, 3, 2, 3])
  USX_FREQ_SEQ_DFLT = ["\": \"", "\": ", "</", "=\"", "\":\"", "://"]
  USX_TEMPLATES = ["tfff-of-tfTtf:rf:rf.fffZ", "tfff-of-tf", "(fff) fff-ffff", "tf:rf:rf", 0]

  USX_ALPHA = 0
  USX_SYM = 1
  USX_NUM = 2
  USX_DICT = 3
  USX_DELTA = 4

  usx_sets = [bytearray(b"\0 etaoinsrlcdhupmbgwfyvkqjxz"),
              bytearray(b"\"{}_<>:\n\0[]\\;'\t@*&?!^|\r~`\0\0\0"),
              bytearray(b"\0,.01925-/34678() =+$%#\0\0\0\0\0")]

  # Stores position of letter in usx_sets.
  # First 3 bits - position in usx_hcodes
  # Next  5 bits - position in self.usx_vcodes
  usx_code_94 = bytearray(94)

  usx_vcodes = bytearray(
    [ 0x00, 0x40, 0x60, 0x80, 0x90, 0xA0, 0xB0,
      0xC0, 0xD0, 0xD8, 0xE0, 0xE4, 0xE8, 0xEC,
      0xEE, 0xF0, 0xF2, 0xF4, 0xF6, 0xF7, 0xF8,
      0xF9, 0xFA, 0xFB, 0xFC, 0xFD, 0xFE, 0xFF ])
  usx_vcode_lens = bytearray(
    [  2,    3,    3,    4,    4,    4,    4,
       4,    5,    5,    6,    6,    6,    7,
       7,    7,    7,    7,    8,    8,    8,
       8,    8,    8,    8,    8,    8,    8 ])

  usx_freq_codes = bytearray([(1 << 5) + 25, (1 << 5) + 26, (1 << 5) + 27, (2 << 5) + 23, (2 << 5) + 24, (2 << 5) + 25])

  NICE_LEN = 5

  RPT_CODE = ((2 << 5) + 26)
  TERM_CODE = ((2 << 5) + 27)
  LF_CODE = ((1 << 5) + 7)
  CRLF_CODE = ((1 << 5) + 8)
  CR_CODE = ((1 << 5) + 22)
  TAB_CODE = ((1 << 5) + 14)
  NUM_SPC_CODE = ((2 << 5) + 17)

  UNI_STATE_SPL_CODE = 0xF8
  UNI_STATE_SPL_CODE_LEN = 5
  UNI_STATE_SW_CODE = 0x80
  UNI_STATE_SW_CODE_LEN = 2

  SW_CODE = 0
  SW_CODE_LEN = 2

  USX_OFFSET_94 = 33

  is_inited = 0
  def init_coder(self):
    if self.is_inited == 1:
      return
    for i in range(3):
      for j in range(28):
        c = self.usx_sets[i][j]
        if c != 0 and c > 32:
          self.usx_code_94[c - self.USX_OFFSET_94] = (i << 5) + j
          if c >= 97 and c <= 122: # a - z
            self.usx_code_94[c - self.USX_OFFSET_94 - (97 - 65)] = (i << 5) + j
    self.is_inited = 1

  usx_mask = bytearray([0x80, 0xC0, 0xE0, 0xF0, 0xF8, 0xFC, 0xFE, 0xFF])
  def append_bits(self, out, ol, code, clen):
    while clen > 0:
      cur_bit = ol % 8
      blen = clen
      a_byte = code & self.usx_mask[blen - 1]
      a_byte >>= cur_bit
      if blen + cur_bit > 8:
        blen = (8 - cur_bit)
      if cur_bit == 0:
        out[ol >> 3] = a_byte
      else:
        out[ol >> 3] |= a_byte
      code <<= blen
      ol += blen
      clen -= blen
    return ol

  def append_switch_code(self, out, ol, state):
    if state == self.USX_DELTA:
      ol = self.append_bits(out, ol, self.UNI_STATE_SPL_CODE, self.UNI_STATE_SPL_CODE_LEN)
      ol = self.append_bits(out, ol, self.UNI_STATE_SW_CODE, self.UNI_STATE_SW_CODE_LEN)
    else:
      ol = self.append_bits(out, ol, self.SW_CODE, self.SW_CODE_LEN)
    return ol

  def append_code(self, out, ol, code, state, usx_hcodes, usx_hcode_lens):
    hcode = code >> 5
    vcode = code & 0x1F
    if usx_hcode_lens[hcode] == 0 and hcode != self.USX_ALPHA:
      return ol, state
    if hcode == self.USX_ALPHA:
      if state != self.USX_ALPHA:
        ol = self.append_switch_code(out, ol, state)
        ol = self.append_bits(out, ol, usx_hcodes[self.USX_ALPHA], usx_hcode_lens[self.USX_ALPHA])
        state = self.USX_ALPHA
    elif hcode == self.USX_SYM:
      ol = self.append_switch_code(out, ol, state)
      ol = self.append_bits(out, ol, usx_hcodes[self.USX_SYM], usx_hcode_lens[self.USX_SYM])
    elif hcode == self.USX_NUM:
      if state != self.USX_NUM:
        ol = self.append_switch_code(out, ol, state)
        ol = self.append_bits(out, ol, usx_hcodes[self.USX_NUM], usx_hcode_lens[self.USX_NUM])
        if self.usx_sets[hcode][vcode] >= 48 and self.usx_sets[hcode][vcode] <= 57:
          state = self.USX_NUM
    return self.append_bits(out, ol, self.usx_vcodes[vcode], self.usx_vcode_lens[vcode]), state

  count_bit_lens = bytearray([2, 4, 7, 11, 16])
  count_adder = [4, 20, 148, 2196, 67732]
  # First five bits are code and Last three bits of codes represent length
  count_codes = bytearray([0x01, 0x82, 0xC3, 0xE4, 0xF4])
  def encodeCount(self, out, ol, count):
    for i in range(5):
      if count < self.count_adder[i]:
        ol = self.append_bits(out, ol, (self.count_codes[i] & 0xF8), self.count_codes[i] & 0x07)
        count16 = (count - (self.count_adder[i - 1] if i > 0 else 0)) << (16 - self.count_bit_lens[i])
        if (self.count_bit_lens[i] > 8):
          ol = self.append_bits(out, ol, count16 >> 8, 8)
          ol = self.append_bits(out, ol, count16 & 0xFF, self.count_bit_lens[i] - 8)
        else:
          ol = self.append_bits(out, ol, count16 >> 8, self.count_bit_lens[i])
        return ol
    return ol

  uni_bit_len = bytearray([6, 12, 14, 16, 21])
  uni_adder = [0, 64, 4160, 20544, 86080]

  def encodeUnicode(self, out, ol, code, prev_code):
    # First five bits are code and Last three bits of codes represent length
    # codes[8] =:0x00, 0x42, 0x83, 0xA3, 0xC3, 0xE4, 0xF5, 0xFD};
    codes = bytearray([0x01, 0x82, 0xC3, 0xE4, 0xF5, 0xFD])
    till = 0
    orig_ol = ol
    diff = code - prev_code
    if diff < 0:
      diff = -diff
    #printf("%ld, ", code)
    #printf("Diff: %d\n", diff)
    for i in range(5):
      till += (1 << self.uni_bit_len[i])
    if diff < till:
        ol = self.append_bits(out, ol, (codes[i] & 0xF8), codes[i] & 0x07)
        #if (diff):
        ol = self.append_bits(out, ol, 0x80 if prev_code > code else 0, 1)
        val = diff - self.uni_adder[i]
        #printf("Val: %d\n", val)
        if self.uni_bit_len[i] > 16:
          val <<= (24 - self.uni_bit_len[i])
          ol = self.append_bits(out, ol, val >> 16, 8)
          ol = self.append_bits(out, ol, (val >> 8) & 0xFF, 8)
          ol = self.append_bits(out, ol, val & 0xFF, self.uni_bit_len[i] - 16)
        elif self.uni_bit_len[i] > 8:
          val <<= (16 - self.uni_bit_len[i])
          ol = self.append_bits(out, ol, val >> 8, 8)
          ol = self.append_bits(out, ol, val & 0xFF, self.uni_bit_len[i] - 8)
        else:
          val <<= (8 - self.uni_bit_len[i])
          ol = self.append_bits(out, ol, val & 0xFF, self.uni_bit_len[i])
        #printf("bits:%d\n", ol-orig_ol)
        return ol
    return ol

  def readUTF8(self, input, ilen, l):
    ret = 0
    if isinstance(input, str):
      ret = ord(input[l])
      return ret, 1
    utf8len = 0
    if l < (ilen - 1) and (input[l] & 0xE0) == 0xC0 and (input[l + 1] & 0xC0) == 0x80:
      utf8len = 2
      ret = (input[l] & 0x1F)
      ret <<= 6
      ret += (input[l + 1] & 0x3F)
      if ret < 0x80:
        ret = 0
    elif l < (ilen - 2) and (input[l] & 0xF0) == 0xE0 and (input[l + 1] & 0xC0) == 0x80 \
            and (input[l + 2] & 0xC0) == 0x80:
      utf8len = 3
      ret = (input[l] & 0x0F)
      ret <<= 6
      ret += (input[l + 1] & 0x3F)
      ret <<= 6
      ret += (input[l + 2] & 0x3F)
      if ret < 0x0800:
        ret = 0
    elif l < (ilen - 3) and (input[l] & 0xF8) == 0xF0 and (input[l + 1] & 0xC0) == 0x80 \
            and (input[l + 2] & 0xC0) == 0x80 and (input[l + 3] & 0xC0) == 0x80:
      utf8len = 4
      ret = (input[l] & 0x07)
      ret <<= 6
      ret += (input[l + 1] & 0x3F)
      ret <<= 6
      ret += (input[l + 2] & 0x3F)
      ret <<= 6
      ret += (input[l + 3] & 0x3F)
      if ret < 0x10000:
        ret = 0
    return ret, utf8len

  def matchOccurance(self, input, ilen, l, out, ol, state, usx_hcodes, usx_hcode_lens):
    longest_dist = 0
    longest_len = 0
    for j in range(l - self.NICE_LEN, -1, -1):
      k = l
      while k < ilen and j + k - l < l:
        if input[k] != input[j + k - l]:
          break
        k = k + 1
      while ((ord(input[k]) if isinstance(input, str) else input[k]) >> 6) == 2:
        k = k - 1 # Skip partial UTF-8 matches
      #if (in[k - 1] >> 3) == 0x1E or (in[k - 1] >> 4) == 0x0E or (in[k - 1] >> 5) == 0x06
      #  k = k - 1
      if k - l > self.NICE_LEN - 1:
        match_len = k - l - self.NICE_LEN
        match_dist = l - j - self.NICE_LEN + 1
        if match_len > longest_len:
          longest_len = match_len
          longest_dist = match_dist
    if longest_len > 0:
      ol = self.append_switch_code(out, ol, state)
      ol = self.append_bits(out, ol, usx_hcodes[self.USX_DICT], usx_hcode_lens[self.USX_DICT])
      #printf("ilen:%d / Dist:%d\n", longest_len, longest_dist)
      ol = self.encodeCount(out, ol, longest_len)
      ol = self.encodeCount(out, ol, longest_dist)
      l += (longest_len + self.NICE_LEN - 1)
      return l, ol
    return -l, ol

  def matchLine(self, input, ilen, l, out, ol, prev_lines, prev_lines_idx, state, usx_hcodes, usx_hcode_lens):
    last_ol = ol
    last_len = 0
    last_dist = 0
    last_ctx = 0
    line_ctr = 0
    j = 0
    while line_ctr <= prev_lines_idx:
      i = k = 0
      prev_line = prev_lines[prev_lines_idx - line_ctr]
      line_len = ilen(prev_line)
      limit = l if line_ctr == 0 else line_len
      for j in range(limit):
        i = l
        k = j
        while k < line_len and k < limit and i < ilen:
          if prev_line[k] != input[i]:
            break
          k = k + 1
          i = i + 1
        while (prev_line[k] >> 6) == 2:
          k = k - 1 # Skip partial UTF-8 matches
        if (k - j) >= self.NICE_LEN:
          if last_len > 0:
            if j > last_dist:
              continue
            #int saving = ((k - j) - last_len) + (last_dist - j) + (last_ctx - line_ctr)
            #if (saving < 0):
            #  //printf("No savng: %d\n", saving)
            #  continue;
            ol = last_ol
          last_len = k - j
          last_dist = j
          last_ctx = line_ctr
          ol = self.append_switch_code(out, ol, state)
          ol = self.append_bits(out, ol, usx_hcodes[self.USX_DICT], usx_hcode_lens[self.USX_DICT])
          ol = self.encodeCount(out, ol, last_len - self.NICE_LEN)
          ol = self.encodeCount(out, ol, last_dist)
          ol = self.encodeCount(out, ol, last_ctx)
          #if ((*ol - last_ol) > (last_len * 4)):
          #  last_len = 0;
          #  *ol = last_ol;
          #}
          #printf("ilen: %d, Dist: %d, Line: %d\n", last_len, last_dist, last_ctx)
          j += last_len
      line_ctr = line_ctr + 1
    if last_len > 0:
      l += (last_len - 1)
      return l, ol
    return -l, ol

  def getBaseCode(self, ch):
    if (ch >= 48 and ch <= 57):
      return (ch - 48) << 4
    elif (ch >= 65 and ch <= 70):
      return (ch - 65 + 10) << 4
    elif (ch >= 97 and ch <= 102):
      return (ch - 97 + 10) << 4
    return 0

  USX_NIB_NUM = 0
  USX_NIB_HEX_LOWER = 1
  USX_NIB_HEX_UPPER = 2
  USX_NIB_NOT = 3
  def getNibbleType(self, ch):
    if (ch >= 48 and ch <= 57):
      return self.USX_NIB_NUM
    elif (ch >= 97 and ch <= 102):
      return self.USX_NIB_HEX_LOWER
    elif (ch >= 65 and ch <= 70):
      return self.USX_NIB_HEX_UPPER
    return self.USX_NIB_NOT

  def append_nibble_escape(self, out, ol, state, usx_hcodes, usx_hcode_lens):
    ol = self.append_switch_code(out, ol, state)
    ol = self.append_bits(out, ol, usx_hcodes[self.USX_NUM], usx_hcode_lens[self.USX_NUM])
    ol = self.append_bits(out, ol, 0, 2)
    return ol

  def compare_arr(self, arr1, arr2, is_str):
    if (is_str):
      return arr1 == arr2
    else:
      if len(arr1) != len(arr2):
        return False
      for i in range(len(arr2)):
        if arr1[i] != arr2[i]:
          return False
    return True

  usx_spl_code = bytearray([0, 0xE0, 0xC0, 0xF0])
  usx_spl_code_len = bytearray([1, 4, 3, 4])

  def unishox2_compress(self, input, ilen, out, usx_hcodes, usx_hcode_lens, usx_freq_seq, usx_templates):

    prev_lines_arr = None
    prev_lines_idx = 0

    # if compressing an element in an array, pass the array as input
    # and index of the array to be decompressed in ilen
    if isinstance(input, list):
      prev_lines_arr = input
      prev_lines_idx = ilen
      input = prev_lines_arr[prev_lines_idx]
      ilen = len(input)

    is_str = isinstance(input, str)

    self.init_coder()
    ol = 0
    prev_uni = 0
    state = self.USX_ALPHA
    is_all_upper = False
    ol = self.append_bits(out, ol, 0x80, 1) # magic bit
    for l in range(ilen):

      if usx_hcode_lens[self.USX_DICT] > 0 and l < (ilen - self.NICE_LEN + 1):
        if prev_lines_arr != None:
          (l, ol) = self.matchLine(input, ilen, l, out, ol, prev_lines_arr, \
                              prev_lines_idx, state, usx_hcodes, usx_hcode_lens)
          if l > 0:
            continue
        else:
          (l, ol) = self.matchOccurance(input, ilen, l, out, ol, state, usx_hcodes, usx_hcode_lens)
          if l > 0:
            continue
        l = -l

      c_in = input[l]
      if (l > 0 and ilen > 4 and l < ilen - 4 and \
            usx_hcode_lens[self.USX_NUM] > 0 and c_in <= '~' if is_str else 126):
        if (c_in == input[l - 1] and c_in == input[l + 1] and c_in == input[l + 2] and \
            c_in == input[l + 3]):
          rpt_count = l + 4
          while (rpt_count < ilen and input[rpt_count] == c_in):
            rpt_count = rpt_count + 1
          rpt_count -= l
          [ol, state] = self.append_code(out, ol, self.RPT_CODE, state, usx_hcodes, usx_hcode_lens)
          ol = self.encodeCount(out, ol, rpt_count - 4)
          l += (rpt_count - 1)
          continue

      if (l <= (ilen - 36) and usx_hcode_lens[self.USX_NUM] > 0):
        hyp_code = '-' if is_str else 45
        hex_type = self.USX_NIB_NUM
        if (input[l + 8] == hyp_code and input[l + 13] == hyp_code
            and input[l + 18] == hyp_code and input[l + 23] == hyp_code):
          uid_pos = l
          for uid_pos in range(l + 36):
            c_uid = ord(input[uid_pos]) if is_str else input[uid_pos]
            if (c_uid == 45):
              continue
            nib_type = self.getNibbleType(c_uid)
            if (nib_type == self.USX_NIB_NOT):
              break
            if (nib_type != self.USX_NIB_NUM):
              if (hex_type != self.USX_NIB_NUM and hex_type != nib_type):
                break
              hex_type = nib_type
          if (uid_pos == l + 36):
            ol = self.append_nibble_escape(out, ol, state, usx_hcodes, usx_hcode_lens)
            ol = self.append_bits(out, ol, (0xF0 if hex_type == self.USX_NIB_HEX_UPPER else 0xC0), \
                    (5 if hex_type == self.USX_NIB_HEX_UPPER else 3))
            for uid_pos in range(l + 36):
              c_uid = ord(input[uid_pos]) if is_str else input[uid_pos]
              if (c_uid != 45): # '-'
                ol = self.append_bits(out, ol, self.getBaseCode(c_uid), 4)
            #printf("GUID:\n")
            l += 35
            continue

      if (l < (ilen - 5) and usx_hcode_lens[self.USX_NUM] > 0):
        hex_type = self.USX_NIB_NUM
        hex_len = 0
        while (l + hex_len < ilen):
          c_uid = ord(input[l + hex_len]) if is_str else input[l + hex_len]
          nib_type = self.getNibbleType(c_uid)
          if (nib_type == self.USX_NIB_NOT):
            break
          if (nib_type != self.USX_NIB_NUM):
            if (hex_type != self.USX_NIB_NUM and hex_type != nib_type):
              break
            hex_type = nib_type
          hex_len = hex_len + 1
        if (hex_len > 10 and hex_type == self.USX_NIB_NUM):
          hex_type = self.USX_NIB_HEX_LOWER
        if ((hex_type == self.USX_NIB_HEX_LOWER or hex_type == self.USX_NIB_HEX_UPPER) and hex_len > 3):
          ol = self.append_nibble_escape(out, ol, state, usx_hcodes, usx_hcode_lens)
          ol = self.append_bits(out, ol, (0x80 if hex_type == self.USX_NIB_HEX_LOWER else 0xE0), \
                    (2 if hex_type == self.USX_NIB_HEX_LOWER else 4))
          ol = self.encodeCount(out, ol, hex_len)
          while (hex_len > 0):
            c_uid = ord(input[l]) if is_str else input[l]
            ol = self.append_bits(out, ol, self.getBaseCode(c_uid), 4)
            l = l + 1
            hex_len -= 1
          l = l - 1
          continue

      if usx_templates != None:
        for i in range(5):
          if isinstance(usx_templates[i], str):
            rem = len(usx_templates[i])
            j = 0
            while j < rem and l + j < ilen:
              c_t = usx_templates[i][j]
              c_in = ord(input[l + j]) if is_str else input[l + j]
              if (c_t == 'f' or c_t == 'F'):
                if (self.getNibbleType(c_in) != (self.USX_NIB_HEX_LOWER if c_t == 'f' else self.USX_NIB_HEX_UPPER) \
                        and self.getNibbleType(c_in) != self.USX_NIB_NUM):
                  break
              elif (c_t == 'r' or c_t == 't' or c_t == 'o'):
                # if c_in does not fall into the number range
                if (c_in < 48 or c_in > (55 if c_t == 'r' else (51 if c_t == 't' else 49))):
                  break
              elif (ord(c_t[0]) != c_in):
                break
              j = j + 1
            if ((j / rem) > 0.66):
              #printf("%s\n", usx_templates[i])
              rem = rem - j
              ol = self.append_nibble_escape(out, ol, state, usx_hcodes, usx_hcode_lens)
              ol = self.append_bits(out, ol, 0, 1)
              ol = self.append_bits(out, ol, (count_codes[i] & 0xF8), count_codes[i] & 0x07)
              ol = self.encodeCount(out, ol, rem)
              for k in range(j):
                c_t = usx_templates[i][k]
                c_in = ord(input[l + k]) if is_str else input[l + k]
                if (c_t == 'f' or c_t == 'F'):
                  ol = self.append_bits(out, ol, self.getBaseCode(c_in), 4)
                elif (c_t == 'r' or c_t == 't' or c_t == 'o'):
                  c_t = 3 if c_t == 'r' else (2 if c_t == 't' else 1)
                  ol = self.append_bits(out, ol, (c_in - 48) << (8 - c_t), c_t)
              l += j
              l -= 1
              break
        if (i < 4):
          continue

      if (usx_freq_seq != None):
        i = 0
        for i in range(6):
          seq_len = len(usx_freq_seq[i])
          if (ilen - seq_len > 0 and l < ilen - seq_len):
            if (usx_hcode_lens[self.usx_freq_codes[i] >> 5] and \
                self.compare_arr(usx_freq_seq[i][0:seq_len], input[l:l + seq_len], is_str)):
              (ol, state) = self.append_code(out, ol, self.usx_freq_codes[i], state, usx_hcodes, usx_hcode_lens)
              l += seq_len
              l -= 1
              break
        if (i < 5):
          continue
      c_in = ord(input[l]) if is_str else input[l]

      is_upper = False
      if (c_in >= 65 and c_in <= 90): # A-Z
        is_upper = True
      else:
        if (is_all_upper):
          is_all_upper = False
          ol = self.append_switch_code(out, ol, state)
          ol = self.append_bits(out, ol, usx_hcodes[self.USX_ALPHA], usx_hcode_lens[self.USX_ALPHA])
          state = self.USX_ALPHA
      if (is_upper and not is_all_upper):
        if (state == self.USX_NUM):
          ol = self.append_switch_code(out, ol, state)
          ol = self.append_bits(out, ol, usx_hcodes[self.USX_ALPHA], usx_hcode_lens[self.USX_ALPHA])
          state = self.USX_ALPHA
        ol = self.append_switch_code(out, ol, state)
        ol = self.append_bits(out, ol, usx_hcodes[self.USX_ALPHA], usx_hcode_lens[self.USX_ALPHA])
        if (state == self.USX_DELTA):
          state = self.USX_ALPHA
          ol = self.append_switch_code(out, ol, state)
          ol = self.append_bits(out, ol, usx_hcodes[self.USX_ALPHA], usx_hcode_lens[self.USX_ALPHA])
      c_next = 0
      if (l + 1 < ilen):
        c_next = ord(input[l + 1]) if is_str else input[l + 1]

      if (c_in >= 32 and c_in <= 126): # ' ' to '~'
        if (is_upper and not is_all_upper):
          ll = l + 4
          while ll >= l and ll < ilen:
            c_u = ord(input[ll]) if is_str else input[ll]
            if (c_u < 65 or c_u > 90): # ~ A-Z
              break
            ll = ll - 1
          if (ll == l-1):
            ol = self.append_switch_code(out, ol, state)
            ol = self.append_bits(out, ol, usx_hcodes[self.USX_ALPHA], usx_hcode_lens[self.USX_ALPHA])
            state = self.USX_ALPHA
            is_all_upper = True
        if (state == self.USX_DELTA):
          ch_idx = " .,".find(chr(c_in))
          if (ch_idx != -1):
            ol = self.append_bits(out, ol, self.UNI_STATE_SPL_CODE, self.UNI_STATE_SPL_CODE_LEN)
            ol = self.append_bits(out, ol, self.usx_spl_code[ch_idx], self.usx_spl_code_len[ch_idx])
            continue
        c_in -= 32
        if (is_all_upper and is_upper):
          c_in += 32
        if (c_in == 0):
          if (state == self.USX_NUM):
            ol = self.append_bits(out, ol, self.usx_vcodes[self.NUM_SPC_CODE & 0x1F], \
                    self.usx_vcode_lens[self.NUM_SPC_CODE & 0x1F])
          else:
            ol = self.append_bits(out, ol, self.usx_vcodes[1], self.usx_vcode_lens[1])
        else:
          c_in = c_in - 1
          (ol, state) = self.append_code(out, ol, self.usx_code_94[c_in], state, usx_hcodes, usx_hcode_lens)
      elif (c_in == 13 and c_next == 10):
        (ol, state) = self.append_code(out, ol, CRLF_CODE, state, usx_hcodes, usx_hcode_lens)
        l = l + 1
      elif (c_in == 10):
        if (state == self.USX_DELTA):
          ol = self.append_bits(out, ol, self.UNI_STATE_SPL_CODE, self.UNI_STATE_SPL_CODE_LEN)
          ol = self.append_bits(out, ol, 0xF0, 4)
        else:
          (ol, state) = self.append_code(out, ol, self.LF_CODE, state, usx_hcodes, usx_hcode_lens)
      elif (c_in == 13):
        (ol, state) = self.append_code(out, ol, self.CR_CODE, state, usx_hcodes, usx_hcode_lens)
      elif (c_in == 9):
        (ol, state) = self.append_code(out, ol, self.TAB_CODE, state, usx_hcodes, usx_hcode_lens)
      else:
        (uni, utf8len) = self.readUTF8(input, ilen, l)
        if (uni > 0):
          l += utf8len
          if (state != self.USX_DELTA):
            (uni2, utf8len) = self.readUTF8(input, ilen, l)
            if (uni2 > 0):
              if (state != self.USX_ALPHA):
                ol = self.append_switch_code(out, ol, state)
                ol = self.append_bits(out, ol, usx_hcodes[self.USX_ALPHA], usx_hcode_lens[self.USX_ALPHA])
              ol = self.append_switch_code(out, ol, state)
              ol = self.append_bits(out, ol, usx_hcodes[self.USX_ALPHA], usx_hcode_lens[self.USX_ALPHA])
              ol = self.append_bits(out, ol, self.usx_vcodes[1], self.usx_vcode_lens[1]) # code for space (' ')
              state = self.USX_DELTA
            else:
              ol = self.append_switch_code(out, ol, state)
              ol = self.append_bits(out, ol, usx_hcodes[self.USX_DELTA], usx_hcode_lens[self.USX_DELTA])
          ol = self.encodeUnicode(out, ol, uni, prev_uni)
          #console.log("%d:%d:%d,", l, utf8len, uni)
          prev_uni = uni
          l = l - 1
        else:
          bin_count = 1
          for bi in range(l + 1, ilen):
            c_bi = input[bi]
            #if (c_bi > 0x1F and c_bi != 0x7F)
            #  break;
            if self.readUTF8(input, ilen, bi) > 0:
              break
            if (bi < (ilen - 4) and c_bi == input[bi - 1] and c_bi == input[bi + 1] \
                  and c_bi == input[bi + 2] and c_bi == input[bi + 3]):
              break
            bin_count = bin_count + 1
          #printf("Bin:%d:%d:%x:%d\n", l, (unsigned char) c_in, (unsigned char) c_in, bin_count)
          ol = self.append_nibble_escape(out, ol, state, usx_hcodes, usx_hcode_lens)
          ol = self.append_bits(out, ol, 0xF8, 5)
          ol = self.encodeCount(out, ol, bin_count)
          while (bin_count > 0):
            ol = self.append_bits(out, ol, input[l], 8)
            l += 1
            bin_count -= 1
          l -= 1

    ret = (ol//8) + (1 if (ol%8) > 0 else 0)
    if ((ol % 8) > 0):
      if (state == self.USX_DELTA):
        ol = self.append_bits(out, ol, self.UNI_STATE_SPL_CODE, self.UNI_STATE_SPL_CODE_LEN)
      (ol, state) = self.append_code(out, ol, self.TERM_CODE, state, usx_hcodes, usx_hcode_lens)
    #printf("\n%ld\n", ol)
    return ret

  def unishox2_compress_simple(self, input, ilen, out):
    return self.unishox2_compress(input, ilen, out, self.USX_HCODES_DFLT, \
              self.USX_HCODE_LENS_DFLT, self.USX_FREQ_SEQ_DFLT, self.USX_TEMPLATES)

  def readBit(self, input1, bit_no):
    return input1[bit_no >> 3] & (0x80 >> (bit_no % 8))

  def read8bitCode(self, input, ilen, bit_no):
    bit_pos = bit_no & 0x07
    char_pos = bit_no >> 3
    code = (input[char_pos] << bit_pos) & 0xFF
    if ((bit_no + bit_pos) < ilen):
      char_pos = char_pos + 1
      code |= input[char_pos] >> (8 - bit_pos)
    else:
      code |= (0xFF >> (8 - bit_pos))
    return code, bit_no

  # Decoder is designed for using less memory, not speed
  SECTION_COUNT = 5
  usx_vsections = bytearray([0x7F, 0xBF, 0xDF, 0xEF, 0xFF])
  usx_vsection_pos = bytearray([0, 4, 8, 12, 20])
  usx_vsection_mask = bytearray([0x7F, 0x3F, 0x1F, 0x0F, 0x0F])
  usx_vsection_shift = bytearray([5, 4, 3, 1, 0])

  # Vertical decoder lookup table - 3 bits code ilen, 5 bytes vertical pos
  # code ilen is one less as 8 cannot be accommodated in 3 bits
  usx_vcode_lookup = bytearray ([
    (1 << 5) + 0,  (1 << 5) + 0,  (2 << 5) + 1,  (2 << 5) + 2,  # Section 1
    (3 << 5) + 3,  (3 << 5) + 4,  (3 << 5) + 5,  (3 << 5) + 6,  # Section 2
    (3 << 5) + 7,  (3 << 5) + 7,  (4 << 5) + 8,  (4 << 5) + 9,  # Section 3
    (5 << 5) + 10, (5 << 5) + 10, (5 << 5) + 11, (5 << 5) + 11, # Section 4
    (5 << 5) + 12, (5 << 5) + 12, (6 << 5) + 13, (6 << 5) + 14,
    (6 << 5) + 15, (6 << 5) + 15, (6 << 5) + 16, (6 << 5) + 16, # Section 5
    (6 << 5) + 17, (6 << 5) + 17, (7 << 5) + 18, (7 << 5) + 19,
    (7 << 5) + 20, (7 << 5) + 21, (7 << 5) + 22, (7 << 5) + 23,
    (7 << 5) + 24, (7 << 5) + 25, (7 << 5) + 26, (7 << 5) + 27
  ])

  def readVCodeIdx(self, input, ilen, bit_no):
    if (bit_no < ilen):
      (code, bit_no) = self.read8bitCode(input, ilen, bit_no)
      i = 0
      while i < self.SECTION_COUNT:
        if (code <= self.usx_vsections[i]):
          vcode = self.usx_vcode_lookup[self.usx_vsection_pos[i] + ((code & self.usx_vsection_mask[i]) >> self.usx_vsection_shift[i])]
          bit_no += ((vcode >> 5) + 1)
          if (bit_no > ilen):
            return 99, bit_no
          return vcode & 0x1F, bit_no
        i = i + 1
    return 99, bit_no

  len_masks = bytearray([0x80, 0xC0, 0xE0, 0xF0, 0xF8, 0xFC, 0xFE, 0xFF])
  def readHCodeIdx(self, input, ilen, bit_no, usx_hcodes, usx_hcode_lens):
    if not usx_hcode_lens[self.USX_ALPHA]:
      return self.USX_ALPHA, bit_no
    if (bit_no < ilen):
      (code, bit_no) = self.read8bitCode(input, ilen, bit_no)
      for code_pos in range(5):
        if (usx_hcode_lens[code_pos] > 0 and \
              (code & self.len_masks[usx_hcode_lens[code_pos] - 1]) == usx_hcodes[code_pos]):
          bit_no += usx_hcode_lens[code_pos]
          return code_pos, bit_no
    return 99, bit_no

  # TODO: Last value check.. Also ilen check in readBit
  def getStepCodeIdx(self, input, ilen, bit_no, limit):
    idx = 0
    while (bit_no < ilen and self.readBit(input, bit_no) > 0):
      idx += 1
      bit_no += 1
      if (idx == limit):
        return idx, bit_no
    if (bit_no >= ilen):
      return 99, bit_no
    bit_no += 1
    return [idx, bit_no]

  def getNumFromBits(self, input, ilen, bit_no, count):
    ret = 0
    while (count > 0 and bit_no < ilen):
      count = count - 1
      ret += (1 << count) if self.readBit(input, bit_no) > 0 else 0
      bit_no += 1
    return ret

  def readCount(self, input, bit_no, ilen):
    idx = 0
    (idx, bit_no) = self.getStepCodeIdx(input, ilen, bit_no, 4)
    if (idx == 99):
      return -1, bit_no
    if (bit_no + self.count_bit_lens[idx] - 1 >= ilen):
      return -1, bit_no
    count = self.getNumFromBits(input, ilen, bit_no, self.count_bit_lens[idx]) \
              + (self.count_adder[idx - 1] if idx > 0 else 0)
    bit_no += self.count_bit_lens[idx]
    return count, bit_no

  def readUnicode(self, input, bit_no, ilen):
    idx = 0
    (idx, bit_no) = self.getStepCodeIdx(input, ilen, bit_no, 5)
    if (idx == 99):
      return 0x7FFFFF00 + 99, bit_no
    if (idx == 5):
      (idx, bit_no) = self.getStepCodeIdx(input, ilen, bit_no, 4)
      return 0x7FFFFF00 + idx, bit_no
    if (idx >= 0):
      sign = self.readBit(input, bit_no) if bit_no < ilen else 0
      bit_no += 1
      if (bit_no + self.uni_bit_len[idx] - 1 >= ilen):
        return 0x7FFFFF00 + 99, bit_no
      count = self.getNumFromBits(input, ilen, bit_no, self.uni_bit_len[idx])
      count += self.uni_adder[idx]
      bit_no += self.uni_bit_len[idx]
      #printf("Sign: %d, Val:%d", sign, count)
      return -count if sign > 0 else count, bit_no
    return 0, bit_no

  def decodeRepeatArray(self, input, ilen, out_arr, out, bit_no, prev_lines_arr, prev_lines_idx,
                              usx_hcodes, usx_hcode_lens, usx_freq_seq, usx_templates):
    dict_len = 0
    (dict_len, bit_no) = self.readCount(input, bit_no, ilen)
    if (dict_len < 0):
      return bit_no, out
    dict_len += self.NICE_LEN
    dist = 0
    (dist, bit_no) = self.readCount(input, bit_no, ilen)
    if (dist < 0):
      return bit_no, out
    ctx = 0
    (ctx, bit_no) = self.readCount(input, bit_no, ilen)
    if (ctx < 0):
      return bit_no, out
    line = None
    if (ctx == 0):
      line = out if out_arr == None else out_arr
    else:
      if (out_arr == None):
        line = self.unishox2_decompress(prev_lines_arr, prev_lines_idx - ctx, None,
                usx_hcodes, usx_hcode_lens, usx_freq_seq, usx_templates)
      else:
        line = bytearray((dist + dict_len) * 2)
        self.unishox2_decompress(prev_lines_arr, prev_lines_idx - ctx, line,
          usx_hcodes, usx_hcode_lens, usx_freq_seq, usx_templates)
    if (out_arr == Nong):
      out += line[dist:dict_len]
    else:
      for i in range(dict_len):
        out_arr[out] = line[dist + i]
        out += 1
    return bit_no, out

  def decodeRepeat(self, input, ilen, out_arr, out, bit_no):
    dict_len = 0
    (dict_len, bit_no) = self.readCount(input, bit_no, ilen)
    if (dict_len < 0):
      return bit_no, out
    dict_len += self.NICE_LEN
    dist = 0
    (dist, bit_no) = self.readCount(input, bit_no, ilen)
    dist += (self.NICE_LEN - 1)
    if (dist < 0):
      return bit_no, out
    #console.log("Decode ilen: %d, dist: %d\n", dict_len - NICE_LEN, dist - NICE_LEN + 1)
    if (out_arr == None):
      out += out[len(out) - dist : dict_len]
    else:
      for i in range(dict_len):
        out_arr[out] = out_arr[out - dist]
        out += 1
    return bit_no, out

  def getHexChar(self, nibble, hex_type):
    if (nibble >= 0 and nibble <= 9):
      return chr(48 + nibble)
    elif (hex_type < 3):
      return chr(97 + nibble - 10)
    return chr(65 + nibble - 10)

  def writeUTF8(self, out_arr, out, uni):
    if (uni < (1 << 11)):
      out_arr[out] = (0xC0 + (uni >> 6))
      out += 1
      out_arr[out] = (0x80 + (uni & 0x3F))
      out += 1
    elif (uni < (1 << 16)):
      out_arr[out] = (0xE0 + (uni >> 12))
      out += 1
      out_arr[out] = (0x80 + ((uni >> 6) & 0x3F))
      out += 1
      out_arr[out] = (0x80 + (uni & 0x3F))
      out += 1
    else:
      out_arr[out] = (0xF0 + (uni >> 18))
      out += 1
      out_arr[out] = (0x80 + ((uni >> 12) & 0x3F))
      out += 1
      out_arr[out] = (0x80 + ((uni >> 6) & 0x3F))
      out += 1
      out_arr[out] = (0x80 + (uni & 0x3F))
      out += 1
    return out

  def appendChar(self, out_arr, out, ch):
    if (out_arr == None):
      out += ch
    else:
      out_arr[out] = ord(ch[0])
      out += 1
    return out

  def appendString(self, out_arr, out, string):
    if (out_arr == None):
      out += str
    else:
      for i in range(len(string)):
        out_arr[out] = ord(string[i])
        out += 1
    return out

  def unishox2_decompress(self, input, ilen, out_arr, usx_hcodes, usx_hcode_lens, usx_freq_seq, usx_templates):

    prev_lines_arr = None
    prev_lines_idx = 0

    self.init_coder()
    bit_no = 1 # ignore the magic bit
    dstate = h = self.USX_ALPHA
    is_all_upper = False
    prev_uni = 0

    # if decompressing an element in an array, pass the array as input
    # and index of the array to be decompressed in ilen
    if isinstance(input, list):
      prev_lines_arr = input
      prev_lines_idx = ilen
      input = prev_lines_arr[prev_lines_idx]
      ilen = len(input)

    ilen <<= 3
    out = "" if out_arr == None else 0 # if out_arr is present, out holds current position of out_arr
    while (bit_no < ilen):
      orig_bit_no = bit_no
      if (dstate == self.USX_DELTA or h == self.USX_DELTA):
        if (dstate != self.USX_DELTA):
          h = dstate
        (delta, bit_no) = self.readUnicode(input, bit_no, ilen)
        if ((delta >> 8) == 0x7FFFFF):
          spl_code_idx = delta & 0x000000FF
          if (spl_code_idx == 99):
            break
          if spl_code_idx == 0:
              out = self.appendChar(out_arr, out, ' ')
              continue
          elif spl_code_idx == 1:
              (h, bit_no) = self.readHCodeIdx(input, ilen, bit_no, usx_hcodes, usx_hcode_lens)
              if (h == 99):
                bit_no = ilen
                continue
              if (h == self.USX_DELTA or h == self.USX_ALPHA):
                dstate = h
                continue
              if (h == self.USX_DICT):
                if (prev_lines_arr == None):
                  (bit_no, out) = self.decodeRepeat(input, ilen, out_arr, out, bit_no)
                else:
                  (bit_no, out) = self.decodeRepeatArray(input, ilen, out_arr, out, bit_no, \
                    prev_lines_arr, prev_lines_idx, usx_hcodes, usx_hcode_lens, usx_freq_seq, usx_templates)
                h = dstate
                continue
          elif spl_code_idx == 2:
              out = self.appendChar(out_arr, out, ',')
              continue
          elif spl_code_idx == 3:
              out = self.appendChar(out_arr, out, '.')
              continue
          elif spl_code_idx == 4:
              out = self.appendChar(out_arr, out, chr(10))
              continue
        else:
          prev_uni += delta
          if (prev_uni > 0):
            if (out_arr == None):
              out += chr(prev_uni)
            else:
              out = self.writeUTF8(out_arr, out, prev_uni)
          #printf("%ld, ", prev_uni)
        if (dstate == self.USX_DELTA and h == self.USX_DELTA):
          continue
      else:
        h = dstate
      c = ""
      is_upper = is_all_upper
      (v, bit_no) = self.readVCodeIdx(input, ilen, bit_no)
      if (v == 99 or h == 99):
        bit_no = orig_bit_no
        break
      if (v == 0 and h != self.USX_SYM):
        if (bit_no >= ilen):
          break
        if (h != self.USX_NUM or dstate != self.USX_DELTA):
          (h, bit_no) = self.readHCodeIdx(input, ilen, bit_no, usx_hcodes, usx_hcode_lens)
          if (h == 99 or bit_no >= ilen):
            bit_no = orig_bit_no
            break
        if (h == self.USX_ALPHA):
          if (dstate == self.USX_ALPHA):
            if (is_all_upper):
              is_upper = is_all_upper = False
              continue
            (v, bit_no) = self.readVCodeIdx(input, ilen, bit_no)
            if (v == 99):
              bit_no = orig_bit_no
              break
            if (v == 0):
                (h, bit_no) = self.readHCodeIdx(input, ilen, bit_no, usx_hcodes, usx_hcode_lens)
                if (h == 99):
                  bit_no = orig_bit_no
                  break
                if (h == self.USX_ALPHA):
                  is_all_upper = True
                  continue
            is_upper = True
          else:
              dstate = self.USX_ALPHA
              continue
        elif (h == self.USX_DICT):
          if (prev_lines_arr == None):
            (bit_no, out) = self.decodeRepeat(input, ilen, out_arr, out, bit_no)
          else:
            (bit_no, out) = self.decodeRepeatArray(input, ilen, out_arr, out, bit_no, \
              prev_lines_arr, prev_lines_idx, usx_hcodes, usx_hcode_lens, usx_freq_seq, usx_templates)
          continue
        elif (h == self.USX_DELTA):
          #printf("Sign: %d, bitno: %d\n", sign, bit_no)
          #printf("Code: %d\n", prev_uni)
          #printf("BitNo: %d\n", bit_no)
          continue
        else:
          if (h != self.USX_NUM or dstate != self.USX_DELTA):
            (v, bit_no) = self.readVCodeIdx(input, ilen, bit_no)
          if (v == 99):
            bit_no = orig_bit_no
            break
          if (h == self.USX_NUM and v == 0):
            (idx, bit_no) = self.getStepCodeIdx(input, ilen, bit_no, 5)
            if (idx == 0):
              (idx, bit_no) = self.getStepCodeIdx(input, ilen, bit_no, 4)
              (rem, bit_no) = self.readCount(input, bit_no, ilen)
              if (rem < 0):
                break
              rem = usx_templates[idx].length - rem
              for j in range(rem):
                c_t = usx_templates[idx][j]
                if (c_t == 'f' or c_t == 'r' or c_t == 't' or c_t == 'o' or c_t == 'F'):
                    nibble_len = (4 if c_t == 'f' or c_t == 'F' else 3 if c_t == 'r' else (2 if c_t == 't' else 1))
                    nibble_char = self.getHexChar(self.getNumFromBits(input, ilen, bit_no, nibble_len), \
                          self.USX_NIB_HEX_LOWER if c_t == 'f' else self.USX_NIB_HEX_UPPER)
                    out = self.appendChar(out_arr, out, nibble_char)
                    bit_no += nibble_len
                else:
                  out = self.appendChar(out_arr, out, c_t)
            elif (idx == 5):
              (bin_count, bit_no) = self.readCount(input, bit_no, ilen)
              if (bin_count < 0):
                break
              while (bin_count > 0):
                bin_byte = chr(self.getNumFromBits(input, ilen, bit_no, 8))
                out = self.appendChar(out_arr, out, bin_byte)
                bit_no += 8
                bin_count -= 1
            else:
              nibble_count = 0
              if (idx == 2 or idx == 4):
                nibble_count = 32
              else:
                (nibble_count, bit_no) = self.readCount(input, bit_no, ilen)
                if (nibble_count < 0):
                  break
              while (nibble_count > 0):
                nibble = self.getNumFromBits(input, ilen, bit_no, 4)
                nibble_char = self.getHexChar(nibble, idx)
                out = self.appendChar(out_arr, out, nibble_char)
                if ((idx == 2 or idx == 4) and (nibble_count == 25 or nibble_count == 21 \
                        or nibble_count == 17 or nibble_count == 13)):
                  out = self.appendChar(out_arr, out, '-')
                bit_no += 4
                nibble_count -= 1
            if (dstate == self.USX_DELTA):
              h = self.USX_DELTA
            continue
      if (is_upper and v == 1):
        h = dstate = self.USX_DELTA # continuous delta coding
        continue
      if (h < 3 and v < 28):
        c = self.usx_sets[h][v]
      if (c >= 97 and c <= 122): # 'a' to 'z'
        dstate = self.USX_ALPHA
        if (is_upper):
          c -= 32
      else:
        if (c >= 48 and c <= 57): # '0' to '9'
          dstate = self.USX_NUM
        elif c == 0:
          if (v == 8):
            out = self.appendString(out_arr, out, "\r\n")
          elif (h == self.USX_NUM and v == 26):
            (count, bit_no) = self.readCount(input, bit_no, ilen)
            if (count < 0):
              break
            count += 4
            rpt_c = out[-1] if out_arr == None else out_arr[out - 1]
            while (count > -1):
              out = self.appendChar(out_arr, out, rpt_c)
          elif (h == self.USX_SYM and v > 24):
            v -= 25
            out = self.appendString(out_arr, out, usx_freq_seq[v])
          elif (h == self.USX_NUM and v > 22 and v < 26):
            v -= (23 - 3)
            out = self.appendString(out_arr, out, usx_freq_seq[v])
          else:
            break # Terminator
          if (dstate == self.USX_DELTA):
            h = self.USX_DELTA
          continue
      if (dstate == self.USX_DELTA):
        h = self.USX_DELTA
      out = self.appendChar(out_arr, out, chr(c))
    return out

  def unishox2_decompress_simple(self, input, ilen):
    return self.unishox2_decompress(input, ilen, None, self.USX_HCODES_DFLT, \
            self.USX_HCODE_LENS_DFLT, self.USX_FREQ_SEQ_DFLT, self.USX_TEMPLATES)
