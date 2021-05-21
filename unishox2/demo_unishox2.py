UNISHOX_VERSION = "2.0"

USX_HCODES_DFLT = bytearray([0x00, 0x40, 0x80, 0xC0, 0xE0])
USX_HCODE_LENS_DFLT = bytearray([2, 2, 2, 3, 3])

USX_HCODES_ALPHA_ONLY = bytearray([0x00, 0x00, 0x00, 0x00, 0x00])
USX_HCODE_LENS_ALPHA_ONLY = bytearray([0, 0, 0, 0, 0])

USX_HCODES_ALPHA_NUM_ONLY = bytearray([0x00, 0x00, 0x80, 0x00, 0x00])
USX_HCODE_LENS_ALPHA_NUM_ONLY = bytearray([1, 0, 1, 0, 0])

USX_HCODES_ALPHA_NUM_SYM_ONLY = bytearray([0x00, 0x80, 0xC0, 0x00, 0x00])
USX_HCODE_LENS_ALPHA_NUM_SYM_ONLY = bytearray([1, 2, 2, 0, 0])

USX_HCODES_FAVOR_ALPHA = bytearray([0x00, 0x80, 0xA0, 0xC0, 0xE0])
USX_HCODE_LENS_FAVOR_ALPHA = bytearray([1, 3, 3, 3, 3])

USX_HCODES_FAVOR_DICT = bytearray([0x00, 0x40, 0xC0, 0x80, 0xE0])
USX_HCODE_LENS_FAVOR_DICT = bytearray([2, 2, 3, 2, 3])

USX_HCODES_FAVOR_SYM = bytearray([0x80, 0x00, 0xA0, 0xC0, 0xE0])
USX_HCODE_LENS_FAVOR_SYM = bytearray([3, 1, 3, 3, 3])

#[{0x00, 0x40, 0xE0, 0xC0, 0x80}],
#[{2, 2, 3, 3, 2}],

USX_HCODES_FAVOR_UMLAUT = bytearray([0x80, 0xA0, 0xC0, 0xE0, 0x00])
USX_HCODE_LENS_FAVOR_UMLAUT = bytearray([3, 3, 3, 3, 1])

USX_HCODES_NO_DICT = bytearray([0x00, 0x40, 0x80, 0x00, 0xC0])
USX_HCODE_LENS_NO_DICT = bytearray([2, 2, 2, 0, 2])

USX_HCODES_NO_UNI = bytearray([0x00, 0x40, 0x80, 0xC0, 0x00])
USX_HCODE_LENS_NO_UNI = bytearray([2, 2, 2, 2, 0])

USX_FREQ_SEQ_DFLT = ["\": \"", "\": ", "</", "=\"", "\":\"", "://"]
USX_FREQ_SEQ_TXT = [" the ", " and ", "tion", " with", "ing", "ment"]
USX_FREQ_SEQ_URL = ["https://", "www.", ".com", "http://", ".org", ".net"]
USX_FREQ_SEQ_JSON = ["\": \"", "\": ", "\",", "}}}", "\":\"", "}}"]
USX_FREQ_SEQ_HTML = ["</", "=\"", "div", "href", "class", "<p>"]
USX_FREQ_SEQ_XML = ["</", "=\"", "\">", "<?xml version=\"1.0\"", "xmlns:", "://"]

USX_TEMPLATES = ["tfff-of-tfTtf:rf:rf.fffZ", "tfff-of-tf", "(fff) fff-ffff", "tf:rf:rf", 0]

USX_PSETS = [
  [USX_HCODES_DFLT, USX_HCODE_LENS_DFLT, USX_FREQ_SEQ_DFLT],                             # 0  USX_PSET_DFLT
  [USX_HCODES_ALPHA_ONLY, USX_HCODE_LENS_ALPHA_ONLY, USX_FREQ_SEQ_TXT],                  # 1  USX_PSET_ALPHA_ONLY
  [USX_HCODES_ALPHA_NUM_ONLY, USX_HCODE_LENS_ALPHA_NUM_ONLY, USX_FREQ_SEQ_TXT],          # 2  USX_PSET_ALPHA_NUM_ONLY
  [USX_HCODES_ALPHA_NUM_SYM_ONLY, USX_HCODE_LENS_ALPHA_NUM_SYM_ONLY, USX_FREQ_SEQ_DFLT], # 3  USX_PSET_ALPHA_NUM_SYM_ONLY
  [USX_HCODES_ALPHA_NUM_SYM_ONLY, USX_HCODE_LENS_ALPHA_NUM_SYM_ONLY, USX_FREQ_SEQ_DFLT], # 4  USX_PSET_ALPHA_NUM_SYM_ONLY_TXT
  [USX_HCODES_FAVOR_ALPHA, USX_HCODE_LENS_FAVOR_ALPHA, USX_FREQ_SEQ_TXT],                # 5  USX_PSET_FAVOR_ALPHA
  [USX_HCODES_FAVOR_DICT, USX_HCODE_LENS_FAVOR_DICT, USX_FREQ_SEQ_DFLT],                 # 6  USX_PSET_FAVOR_DICT
  [USX_HCODES_FAVOR_SYM, USX_HCODE_LENS_FAVOR_SYM, USX_FREQ_SEQ_DFLT],                   # 7  USX_PSET_FAVOR_SYM
  [USX_HCODES_FAVOR_UMLAUT, USX_HCODE_LENS_FAVOR_UMLAUT, USX_FREQ_SEQ_DFLT],             # 8  USX_PSET_FAVOR_UMLAUT
  [USX_HCODES_NO_DICT, USX_HCODE_LENS_NO_DICT, USX_FREQ_SEQ_DFLT],                       # 9  USX_PSET_NO_DICT
  [USX_HCODES_NO_UNI, USX_HCODE_LENS_NO_UNI, USX_FREQ_SEQ_DFLT],                         # 10 USX_PSET_NO_UNI
  [USX_HCODES_NO_UNI, USX_HCODE_LENS_NO_UNI, USX_FREQ_SEQ_TXT],                          # 11 USX_PSET_NO_UNI_FAVOR_TEXT
  [USX_HCODES_DFLT, USX_HCODE_LENS_DFLT, USX_FREQ_SEQ_URL],                              # 12 USX_PSET_URL
  [USX_HCODES_DFLT, USX_HCODE_LENS_DFLT, USX_FREQ_SEQ_JSON],                             # 13 USX_PSET_JSON
  [USX_HCODES_NO_UNI, USX_HCODE_LENS_NO_UNI, USX_FREQ_SEQ_JSON],                         # 14 USX_PSET_JSON_NO_UNI
  [USX_HCODES_DFLT, USX_HCODE_LENS_DFLT, USX_FREQ_SEQ_XML],                              # 15 USX_PSET_XML
  [USX_HCODES_DFLT, USX_HCODE_LENS_DFLT, USX_FREQ_SEQ_HTML]];                            # 16 USX_PSET_HTML

def unishox2_compress_preset(unishox2, input, len, out, pset):
  return unishox2.unishox2_compress(input, len, out, USX_PSETS[pset][0], USX_PSETS[pset][1], USX_PSETS[pset][2], USX_TEMPLATES)

def unishox2_decompress_preset(unishox2, input, len, out, pset):
  return unishox2.unishox2_decompress(input, len, out, USX_PSETS[pset][0], USX_PSETS[pset][1], USX_PSETS[pset][2], USX_TEMPLATES)

if __name__ == "__main__":
  import sys
  from unishox2 import Unishox2
  usx = Unishox2()
  args = sys.argv
  argv = len(args)

  read_size = 4096
  dbuf = bytearray(8192)

  tot_len = ctot = 0
  fp = wfp = 0

  if (argv >= 4 and args[1] == "-c"):
    preset = 0
    if (argv > 4):
      preset = int(args[4])
    tot_len = 0
    ctot = 0
    try:
      fp = open(args[2], "rb")
    except Error as e:
      print(e)
      exit
    try:
      wfp = open(args[3], "wb+")
    except Error as e:
      print(e)
      exit
    bytes_read = 1
    while (bytes_read > 0):
      cbuf = fp.read(read_size)
      if not cbuf:
        break
      bytes_read = len(cbuf)
      if (bytes_read > 0):
        clen = unishox2_compress_preset(cbuf, bytes_read, dbuf, preset)
        ctot += clen
        tot_len += bytes_read
        if (clen > 0):
          wfp.write(bytearray([clen >> 8, clen & 0xFF]))
          wfp.write(dbuf[0:clen])
    perc = (tot_len-ctot)
    perc /= tot_len
    perc *= 100
    print("\nBytes (Compressed/Original=Savings%%): %ld/%ld=".format(ctot, tot_len))
    print("%.2f%%".format(perc))
  elif (argv >= 4 and args[1] == "-d"):
    preset = 0
    if (argv > 4):
      preset = int(args[4], 10)
    try:
      fp = open(args[2], "r")
    except Error as e:
      print(e)
      exit
    try:
      wfp = open(args[3], "w+")
    except Error as e:
      print(e)
      exit
    bytes_read = 1
    while (bytes_read > 0):
      #memset(dbuf, 0, sizeof(dbuf));
      cbuf = fp.read(2)
      if not cbuf:
        break
      len_to_read = cbuf[0] << 8
      len_to_read += cbuf[1]
      cbuf = fp.read(len_to_read)
      if not cbuf:
        break
      bytes_read = len(cbuf)
      if (bytes_read > 0):
          dlen = unishox2_decompress_preset(cbuf, bytes_read, dbuf, preset)
          if (dlen > 0):
            wfp.write(dbuf[0:dlen])
  elif (argv >= 4 and (args[1] == "-g" or args[1] == "-G")):
    preset = 0
    if (argv > 4):
      preset = int(args[4])
    if (args[1] == "-g"):
      preset = 9; # = USX_PSET_NO_DICT;
      try:
        fp = open(args[2], "rb")
      except Error as e:
        print(e)
        exit
      try:
        wfp = open(args[3] + ".js", "wb+")
      except Error as e:
        print(e)
        exit
      tot_len = 0
      ctot = 0
      prev_lines = bytearray([])
      prev_lines_compressed = bytearray([])
      wfp.write("# _UNISHOX2_COMPRESSED__")
      wfp.write(args[3])
      wfp.write("__\n")
      line_ctr = 0
      max_len = 0
      cur_pos = 0
      max_line_length = 1024;
      cbuf = fp.read(max_line_length)
      if not cbuf:
        exit
      while (cbuf):
        len = 0
        while (cbuf[len] != 13 and cbuf[len] != 10):
          len += 1
        cur_pos += len
        cur_pos += 1
        # compress the line and look in previous lines
        # add to linked list
        if (len > 0):
          prev_lines.append(cbuf[0:len])
          clen = unishox2_compress_preset(prev_lines, line_ctr, dbuf, preset)
          if (clen > 0):
              perc = (len-clen)
              perc /= len
              perc *= 100
              #print_compressed(dbuf, clen);
              print("len: {}/{}={}".format(clen, len, perc))
              tot_len += len
              ctot += clen
              if (line_ctr > 0):
                wfp.write(", \n")
              wfp.write("new Uint8Array([")
              for i in range(clen):
                wfp.write(("" if i == 0 else ", ") + dbuf[i])
              wfp.write("])")
              if (len > max_len):
                max_len = len
              prev_lines_compressed.append(dbuf[0:clen])
              print(unishox2_decompress_preset(prev_lines_compressed, line_ctr, null, preset))
          line_ctr += 1
      wfp.write("];\n")
      perc = (tot_len-ctot)
      perc /= tot_len
      perc *= 100
      print("\nBytes (Compressed/Original=Savings%%): {}/{}={}%".format(ctot, tot_len, perc))
  elif (argv == 2 or (argv == 3 and int(args[2]) > 0)):
    pset = 0
    if (argv > 2):
      pset = int(args[2], 10)
    buf_len = usx.unishox2_compress(args[1], len(args[1]), dbuf, USX_PSETS[pset][0], USX_PSETS[pset][1], USX_PSETS[pset][2], USX_TEMPLATES)
    out_str = usx.unishox2_decompress(dbuf, buf_len, None, USX_PSETS[pset][0], USX_PSETS[pset][1], USX_PSETS[pset][2], USX_TEMPLATES)
    input_len = len(args[1])
    print("")
    print("Input: " + args[1])
    print("")
    print("Compressed (Uint8Array) : ", dbuf[0:buf_len])
    print("")
    print("Decompressed: " + out_str)
    print("")
    print("Compression ratio:(" + str(buf_len) + "/" + str(input_len) + " = " + str(round((input_len-buf_len)*1000/input_len) / 10) + "% savings)")
    print("")
  elif (argv >= 4 and (args[1] == "-a" or args[1] == "-A")):
    preset = 0
    if (argv > 4):
      preset = int(args[4])
    if (args[1] == "-a"):
      preset = 9 # = USX_PSET_NO_DICT;
    prev_lines_arr = __import__(args[2])
    print(unishox2_decompress_preset(prev_lines_arr, int(args[3]), None, preset))
  elif (argv == 2 or (argv == 3 and int(args[2]) > 0)):
    pset = 0
    if (argv > 2):
      pset = int(args[2])
    buf_len = usx.unishox2_compress(args[1], args[1].length, dbuf, USX_PSETS[pset][0], USX_PSETS[pset][1], USX_PSETS[pset][2], USX_TEMPLATES)
    out_str = usx.unishox2_decompress(dbuf, buf_len, null, USX_PSETS[pset][0], USX_PSETS[pset][1], USX_PSETS[pset][2], USX_TEMPLATES)
    input_len = len(args[1])
    print("")
    print("Input: " + args[1])
    print("")
    print("Compressed (Uint8Array) : " + dbuf.slice(0, buf_len))
    print("")
    print("Decompressed: " + out_str)
    print("")
    print("Compression ratio:(" + buf_len + "/" + input_len + " = " + (Math.round((input_len-buf_len)*1000/input_len) / 10) + "% savings)")
    print("")
  else:
    print("Unishox (byte format version: {})".format(UNISHOX_VERSION))
    print("----------------------------------")
    print("Usage: node demo_unishox2 \"string\" [preset_number]")
    print("              (or)")
    print("       unishox2 [action] [in_file] [out_file] [preset_number]")
    print("")
    print("         [action]:")
    print("         -t    run tests")
    print("         -c    compress")
    print("         -d    decompress")
    print("         -g    generate Uint8Array file")
    print("         -G    generate Uint8Array file using additional compression (slower)")
    print("         -a    Decompress specific line of a file generated with -g")
    print("         -A    Decompress specific line of a file generated with -G")
    print("")
    print("         [preset_number]:")
    print("         0    Optimum - favors all including JSON, XML, URL and HTML (default)")
    print("         1    Alphabets [a-z], [A-Z] and space only")
    print("         2    Alphanumeric [a-z], [A-Z], [0-9], [.,/()-=+$%%#] and space only")
    print("         3    Alphanumeric and symbols only")
    print("         4    Alphanumeric and symbols only (Favor English text)")
    print("         5    Favor Alphabets")
    print("         6    Favor Dictionary coding")
    print("         7    Favor Symbols")
    print("         8    Favor Umlaut")
    print("         9    No dictionary")
    print("         10   No Unicode")
    print("         11   No Unicode, favour English text")
    print("         12   Favor URLs")
    print("         13   Favor JSON")
    print("         14   Favor JSON (No Unicode)")
    print("         15   Favor XML")
    print("         16   Favor HTML")
    exit(1)
