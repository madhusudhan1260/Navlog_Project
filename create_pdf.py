from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

W, H = A4

# ================= COMMON HELPER FUNCTIONS =================

def text(c, x, y, value, font="Courier", size=8.5):
    c.setFont(font, size)
    c.drawString(x, y, str(value))

def text_right(c, x, y, value, font="Courier", size=8.5):
    c.setFont(font, size)
    c.drawRightString(x, y, str(value))

def text_center(c, x, y, value, font="Courier", size=8.5):
    c.setFont(font, size)
    c.drawCentredString(x, y, str(value))

def frame(c):
    c.setLineWidth(1)
    c.rect(35, 35, W-70, H-70)
    text_right(c, W-50, H-25, "VOHS - VOCI   VTKVR", font="Courier-Bold", size=10)


# ================= PAGE 1 =================

def page1(c, data=None):
    frame(c)
    text_center(c, W/2, 795, "----- VTKVR (HA4T) 01JUL26 NAV LOG/ OPS FPL FOR ETD 0730Z (ETA 0834Z) -----", font="Courier-Bold", size=9)

    y = 765
    text(c, 55, y, "DEP   : VOHS - SHAMSHABAD")
    text(c, 275, y, "DIST       : 456NM")
    text(c, 455, y, "TRACK : 074 DEG")

    y -= 15
    text(c, 55, y, "DEST  : VOCI - COCHIN INTERNATIONAL")
    text(c, 275, y, "CRUISE     : IFR 280 KIAS/M0.76 - MACH 0.82 @")
    
    y -= 12
    text(c, 390, y, "FL400 - 300 KIAS/M0.82")

    y -= 15
    text(c, 55, y, "MAIN ROUTE : FL400 - 300 KIAS/M0.82 HIA Q21 BIA W118 CIA")

    y -= 18
    text(c, 55, y, "PIC : CAPT VIVEK SONDHI", font="Courier-Bold")
    text(c, 320, y, "FO  : CAPT VAIBHAV THAKUR", font="Courier-Bold")

    left_fuel = [
        "COMPUTED FUEL  :      9500 LBS",
        "MIN. TRIP FUEL :     5530 LBS",
        "MAX. TRIP FUEL :    12033 LBS",
        "TOP CLIMB TEMP : FL 380 (ISA: -56°C)"
    ]

    # FIX 1 (kept): Label is TOTAL BURN (2526 LBS = Trip 2401 + Taxi 125)
    right_fuel = [
        "BLOCK FUEL    :      2526 LBS",
        "TAKE OFF FUEL :      9375 LBS",
        "LANDING FUEL  :      6974 LBS",
        "WIND          : 14KT TAIL (074°/041)"
    ]

    y = 690
    for a, b in zip(left_fuel, right_fuel):
        text(c, 55, y, a)
        text(c, 320, y, b)
        y -= 14

    text_center(c, W/2, 625, "------------ PLAN TIME & FUEL -------------------------------- PLAN WT (in LBS) ------------", font="Courier-Bold", size=8.5)

    # FIX 2: ALTN1 relabeled from VOCI to VOBL (VOCI is the destination, not an alternate)
    # FIX 3 (reverted): Contingency time kept at 0:06 -- confirmed correct, since
    #   Trip(1:04)+Taxi(0:10)+Contingency(0:06)+Final Reserve(0:30)+XTRA(2:03)+ALTN1(0:37) = 4:30 = ENDURANCE
    # FIX 4: ALTN2 time corrected from 0:14 to 0:15 to match the VOCB alternate route table's
    #   cumulative ETE (0:01+0:01+0:09+0:04+0:00 = 0:15)
    plan_rows = [
        ("TRIP",               ": 1:04",  "2401 LBS"),
        ("TAXI",               ": 0:10",   "125 LBS"),
        ("CONTINGENCY 5%",     ": 0:06",   "120 LBS"),
        ("FINAL RESERVE FUEL", ": 0:30",  "1464 LBS"),
        ("XTRA",               ": 2:03",  "3970 LBS"),
        ("ALTN1 - VOBL",       ": 0:37",  "1420 LBS"),
        ("ALTN2 - VOCB",       ": 0:15",   "540 LBS"),
    ]

    y_p = 605
    for label, time_val, lbs_val in plan_rows:
        text(c, 55, y_p, label)
        text(c, 195, y_p, time_val)
        text(c, 255, y_p, lbs_val)
        y_p -= 14
    
    text(c, 195, y_p, "---------------------")
    y_p -= 14
    text(c, 55, y_p, "ENDURANCE")
    text(c, 195, y_p, ": 4:30")
    text(c, 255, y_p, "9500 LBS")

    # FIX 4: MIN DIVERT FUEL relabeled from VOCI to VOBL (matches ALTN1 fix above)
    weight_lines = [
        "BASIC WT    :      23912 LBS",
        "LOAD        :        185 LBS",
        "ZERO FUEL   :      24097 LBS",
        "T.OFF WT    :      33472 LBS",
        "LAND WT     :      31071 LBS",
        "",
        "ALTN : 205NM",
        "MIN DIVERT FUEL (VOBL): 2884 LBS",
        "FIRST ALTN ROUTE : CIA W118 CCB W43 BIA",
        "SECOND ALTN ROUTE : CIA W118 CCB"
    ]

    y_w = 605
    for line in weight_lines:
        text(c, 320, y_w, line)
        y_w -= 14

    text_center(c, W/2, 455, "------------ DIFFERENT LEVEL CALCULATION --------------------------- ACTUALS ------------", font="Courier-Bold", size=8.5)

    y_calc = 432
    text(c, 75, y_calc, "FL", font="Courier-Bold")
    text(c, 125, y_calc, "WC", font="Courier-Bold")
    text(c, 175, y_calc, "TIME", font="Courier-Bold")
    text(c, 240, y_calc, "TRIP", font="Courier-Bold")

    calc_data = [
        ("FL 340", "T10", "",       "2598 LBS"), 
        ("FL 360", "T11", "(0:00)", "2544 LBS"), 
        ("FL 380", "T12", "",       "2468 LBS"), 
        ("FL 400", "T14", "(0:00)", "2401 LBS"), 
        ("FL 430", "T17", "",       "2353 LBS")  
    ]

    # --- Print Row 1 (FL 340) -> CHOCKS OFF & LANDING
    y_calc -= 16
    text(c, 65, y_calc, calc_data[0][0])
    text(c, 125, y_calc, calc_data[0][1])
    text(c, 170, y_calc, calc_data[0][2])
    text(c, 235, y_calc, calc_data[0][3])
    text(c, 335, y_calc, "CHOCKS OFF   : ______")
    text(c, 455, y_calc, "LANDING    : ______")

    # --- Print Row 2 (FL 360) -> CHOCKS ON & AIRBORNE
    y_calc -= 14
    text(c, 65, y_calc, calc_data[1][0])
    text(c, 125, y_calc, calc_data[1][1])
    text(c, 170, y_calc, calc_data[1][2])
    text(c, 235, y_calc, calc_data[1][3])
    text(c, 335, y_calc, "CHOCKS ON    : ______")
    text(c, 455, y_calc, "AIRBORNE   : ______")

    # --- Print Row 3 (FL 380) -> BLOCK TIME & FLT TIME
    y_calc -= 14
    text(c, 65, y_calc, calc_data[2][0])
    text(c, 125, y_calc, calc_data[2][1])
    text(c, 170, y_calc, calc_data[2][2])
    text(c, 235, y_calc, calc_data[2][3])
    text(c, 335, y_calc, "BLOCK TIME   : ______")
    text(c, 455, y_calc, "FLT TIME   : ______")

    # --- Print Row 4 (FL 400) -> BLOCK FUEL & FIC-ADC
    y_calc -= 14
    text(c, 65, y_calc, calc_data[3][0])
    text(c, 125, y_calc, calc_data[3][1])
    text(c, 170, y_calc, calc_data[3][2])
    text(c, 235, y_calc, calc_data[3][3])
    text(c, 335, y_calc, "BLOCK FUEL   : ______")
    text(c, 455, y_calc, "FIC-ADC    : ______")

    # --- Print Row 5 (FL 430) -> LANDING FUEL (under BLOCK FUEL column)
    y_calc -= 14
    text(c, 65, y_calc, calc_data[4][0])
    text(c, 125, y_calc, calc_data[4][1])
    text(c, 170, y_calc, calc_data[4][2])
    text(c, 235, y_calc, calc_data[4][3])
    text(c, 335, y_calc, "LANDING FUEL : ______")
    
    # Briefing fields block
    y_brief = y_calc - 24
    briefs = ["ATC CLEARANCE :", "DEP ATIS :", "ARR ATIS :", "DEST ALTN ATIS :"]
    for brief in briefs:
        text(c, 55, y_brief, brief, font="Courier-Bold")
        y_brief -= 28

    # V Speeds row
    y_v_speeds = y_brief - 10
    text(c, 55, y_v_speeds, "V1: ______________   VR: ______________   V2: ______________   VFTO: ______________   VREF: ______________", font="Courier-Bold", size=7.5)

    c.setLineWidth(0.5)
    c.line(55, y_v_speeds - 15, W-55, y_v_speeds - 15)

    # Certification text block coordinates
    cert_y = y_v_speeds - 32
    cert_1 = "I certify that all my licenses, ratings etc are current / valid and I am legally/ medically fit for operating flight. I meet the qualification"
    cert_2 = "requirements to operate to concerned airfields as per category/routes indicated per OM D. I have read and understood the operations"
    cert_3 = "manual, OPS supplements, emails, NOTAMS and required compliance. (cars, circulars, aips, etc).BA test complied as per car section 5"
    cert_4 = "series F part 3."
    
    text_center(c, W/2, cert_y, cert_1, font="Helvetica", size=7.2)
    text_center(c, W/2, cert_y - 10, cert_2, font="Helvetica", size=7.2)
    text_center(c, W/2, cert_y - 20, cert_3, font="Helvetica", size=7.2)
    text_center(c, W/2, cert_y - 30, cert_4, font="Helvetica", size=7.2)

    # Signature line positioned a fixed, modest distance below the certification
    sig_y = cert_y - 30 - 45
    text_right(c, W-55, sig_y, "(PILOT/COPILOT SIGNATURE)", font="Courier-Bold", size=8.5)


# ================= PAGE 2 (NAVLOG WAYPOINT TABLE - FULL) =================

def page2(c, data=None):
    frame(c)
    col_x = [35, 110, 145, 165, 185, 215, 235, 273, 291, 311, 331, 351, 373, 398, 423, 445, 467, 489, 514, 539, 560]
    
    y = 790
    row_h = 16
    c.setLineWidth(0.5)
    
    c.rect(35, y - row_h, W-70, row_h)
    text_center(c, (col_x[5]+col_x[8])/2, y - 11, "WIND", font="Courier-Bold", size=7.5)
    text_center(c, (col_x[8]+col_x[10])/2, y - 11, "SPD KT", font="Courier-Bold", size=7.5)
    text_center(c, (col_x[10]+col_x[12])/2, y - 11, "DIST NM", font="Courier-Bold", size=7.5)
    text_center(c, (col_x[12]+col_x[14])/2, y - 11, "FUEL LB", font="Courier-Bold", size=7.5)
    text_center(c, (col_x[14]+col_x[17])/2, y - 11, "TIME", font="Courier-Bold", size=7.5)
    
    for idx in [5, 8, 10, 12, 14, 17, 18, 19]:
        c.line(col_x[idx], y, col_x[idx], y - row_h)
    y -= row_h
    
    c.rect(35, y - row_h, W-70, row_h)
    headers = [
        "WAYPOINT", "AIRWAY", "HDG", "CRS", "ALT", "CMP", "DIR/SPD", "ISA", 
        "TAS", "GS", "LEG", "REM", "USED", "REM", "LEG", "REM", "ETE", "ETA", "ACT"
    ]
    for i, h_txt in enumerate(headers):
        if i in (17, 18):
            text_center(c, (col_x[i]+col_x[i+1])/2, y - 8, h_txt, font="Courier-Bold", size=6)
        else:
            text_center(c, (col_x[i]+col_x[i+1])/2, y - 11, h_txt, font="Courier-Bold", size=6.5)
    
    text_center(c, (col_x[17]+col_x[18])/2, y - 14.5, "ATA", font="Courier-Bold", size=5)
    text_center(c, (col_x[18]+col_x[19])/2, y - 14.5, "FUEL", font="Courier-Bold", size=5)
    
    for i in range(len(col_x)):
        c.line(col_x[i], y, col_x[i], y - row_h)
    y -= row_h
    
    main_route_logs = [
        ("VOHS", "", "-", "-", "2030", "-", "-", "+14", "-", "-", "-", "456", "125", "9375", "-", "1:04", "-", "", ""),
        ("HIA HYDERABAD\n113.8", "DCT", "247", "244", "3400", "H20", "276/024", "+14", "277", "258", "1", "455", "155", "9345", "0:01", "1:03", "0:01", "", ""),
        ("LURGI", "Q21", "177", "175", "FL262", "T5", "283/017", "+17", "353", "358", "61", "394", "806", "8694", "0:10", "0:53", "0:11", "", ""),
        ("PADBI", "Q21", "188", "189", "FL392", "T11", "061/018", "+15", "447", "458", "59", "335", "1196", "8304", "0:08", "0:45", "0:19", "", ""),
        ("-TOC-", "Q21", "186", "190", "FL400", "T14", "072/029", "+4", "439", "454", "5", "330", "1220", "8280", "0:00", "0:45", "0:19", "", ""),
        ("RITNU", "Q21", "186", "190", "FL400", "T14", "071/031", "+3", "474", "487", "21", "309", "1302", "8198", "0:03", "0:42", "0:22", "", ""),
        ("TELUV", "Q21", "186", "190", "FL400", "T14", "071/033", "+3", "474", "488", "39", "270", "1461", "8039", "0:05", "0:37", "0:27", "", ""),
        ("BIA BENGALURU\n116.8", "Q21", "204", "208", "FL400", "T26", "075/042", "+3", "473", "499", "64", "206", "1708", "7792", "0:07", "0:30", "0:34", "", ""),
        ("AKTIM", "W118", "181", "186", "FL400", "T14", "075/047", "+3", "473", "487", "69", "137", "1980", "7520", "0:09", "0:21", "0:43", "", ""),
        ("-TOD-", "W118", "204", "208", "FL400", "T31", "075/048", "+2", "473", "504", "42", "95", "2141", "7359", "0:05", "0:16", "0:48", "", ""),
        ("SATBI", "W118", "207", "212", "FL393", "T34", "073/048", "+2", "401", "435", "2", "93", "2147", "7353", "0:00", "0:16", "0:48", "", ""),
        ("CCB COIMBATORE\n112.9", "W118", "205", "208", "FL289", "T32", "076/028", "+12", "438", "470", "25", "68", "2221", "7279", "0:03", "0:13", "0:51", "", ""),
        ("CIA COCHIN 113.5", "W118", "220", "218", "600", "T5", "293/010", "+16", "313", "317", "66", "2", "2512", "6988", "0:13", "0:00", "1:04", "", ""),
        ("VOCI", "DCT", "085", "086", "30", "T7", "297/009", "+12", "221", "229", "2", "-", "2526", "6974", "0:00", "-", "1:04", "", "")
    ]
    
    def draw_rows(data_list):
        nonlocal y
        for row in data_list:
            is_multiline = "\n" in row[0]
            current_h = row_h * 1.5 if is_multiline else row_h
            c.rect(35, y - current_h, W-70, current_h)
            
            for idx, val in enumerate(row):
                if idx == 0 and is_multiline:
                    lines = val.split("\n")
                    text(c, col_x[idx] + 3, y - 11, lines[0], size=6.2)
                    text(c, col_x[idx] + 3, y - 20, lines[1], size=6.2)
                else:
                    text_center(c, (col_x[idx]+col_x[idx+1])/2, y - (15 if is_multiline else 11), val, size=6.5)
            
            for idx in range(len(col_x)):
                c.line(col_x[idx], y, col_x[idx], y - current_h)
            y -= current_h

    draw_rows(main_route_logs)
    
    y -= 5
    c.rect(35, y - 20, W-70, 20)
    text(c, 40, y - 14, "Alternate route for VOCI,VOBL       Route CIA W118 CCB W43 BIA", font="Courier-Bold", size=7.5)
    y -= 20
    
    alt_route_1 = [
        ("CIA COCHIN 113.5", "DCT", "267", "266", "2100", "H8", "294/010", "+12", "286", "278", "2", "203", "166", "6808", "0:00", "0:37", "-", "", ""),
        ("-TOC-", "W118", "036", "038", "FL190", "T7", "282/015", "+14", "322", "328", "30", "173", "554", "6420", "0:06", "0:31", "0:06", "", ""),
        ("CCB COIMBATORE\n112.9", "W118", "037", "039", "FL190", "H1", "314/008", "+18", "341", "340", "36", "137", "756", "6218", "0:06", "0:25", "0:12", "", ""),
        ("LENBO", "W43", "012", "013", "FL190", "H5", "309/011", "+18", "341", "336", "25", "112", "898", "6076", "0:05", "0:20", "0:17", "", ""),
        ("UGABA", "W43", "012", "013", "FL190", "H4", "306/009", "+18", "341", "337", "44", "68", "1140", "5834", "0:07", "0:13", "0:24", "", ""),
        ("-TOD-", "W43", "020", "021", "FL190", "H1", "295/007", "+18", "341", "341", "31", "37", "1314", "5660", "0:06", "0:07", "0:30", "", ""),
        ("BIA BENGALURU\n116.8", "W43", "018", "022", "3000", "H0", "276/021", "+16", "287", "286", "36", "1", "1536", "5438", "0:07", "0:00", "0:37", "", ""),
        ("VOBL", "DCT", "139", "135", "3003", "T19", "274/026", "+15", "264", "283", "1", "-", "1545", "5429", "0:00", "-", "0:37", "", "")
    ]
    draw_rows(alt_route_1)
    
    y -= 5
    c.rect(35, y - 20, W-70, 20)
    text(c, 40, y - 14, "Alternate route for VOCI,VOCB       Route CIA W118 CCB", font="Courier-Bold", size=7.5)
    y -= 20
    
    alt_route_2 = [
        ("CIA COCHIN 113.5", "DCT", "267", "266", "2100", "H8", "294/010", "+12", "286", "278", "2", "67", "166", "6808", "0:01", "0:14", "0:01", "", ""),
        ("-TOC-", "W118", "035", "038", "7000", "T5", "291/017", "+12", "286", "292", "5", "62", "259", "6715", "0:01", "0:13", "0:02", "", "")
    ]
    draw_rows(alt_route_2)

    alt_route_2_remain = [
        ("-TOD-", "W118", "034", "038", "7000", "T7", "287/022", "+13", "283", "290", "47", "15", "566", "6408", "0:09", "0:04", "0:11", "", ""),
        ("CCB COIMBATORE\n112.9", "W118", "035", "039", "1500", "T9", "267/019", "+13", "212", "221", "14", "1", "660", "6314", "0:04", "0:00", "0:15", "", ""),
        ("VOCB", "DCT", "230", "229", "1330", "H13", "245/013", "+13", "219", "206", "1", "-", "665", "6309", "0:00", "-", "0:15", "", "")
    ]
    draw_rows(alt_route_2_remain)

    y -= 25
    text(c, 35, y, "AIRPORT INFO", font="Courier-Bold", size=9.5)
    y -= 12
    
    apt_x = [35, 75, 115, 155, 195, 250, 310, 365, 410, 455, 500, 560]
    
    c.rect(35, y - row_h, W-70, row_h)
    apt_headers = ["", "Airport", "ETA", "ATIS", "TWR/CTAF", "CLR", "GND", "ELEV", "LONGEST RWY", ""]
    for i, a_hdr in enumerate(apt_headers[:-1]):
        if a_hdr != "" and i != 8:
            text_center(c, (apt_x[i]+apt_x[i+1])/2, y - 11, a_hdr, font="Courier-Bold", size=7)
            
    text_center(c, (apt_x[8]+apt_x[10])/2, y - 11, "LONGEST RWY", font="Courier-Bold", size=7)
    
    for idx in range(len(apt_x) - 1):
        if idx == 9:
            continue
        c.line(apt_x[idx], y, apt_x[idx], y - row_h)
    y -= row_h
    
    airport_data = [
        ("DEP", "VOHS", "-", "126.475", "118.45", "121.625", "121.85", "2030", "09R / 27L", "13976 ft"),
        ("DEST", "VOCI", "0834Z", "126.2", "118.8", "N/A", "121.75", "30", "09 / 27", "11155 ft")
    ]
    
    for row in airport_data:
        c.rect(35, y - row_h, W-70, row_h)
        text_center(c, (apt_x[0]+apt_x[1])/2, y - 11, row[0], font="Courier-Bold", size=7)
        text_center(c, (apt_x[1]+apt_x[2])/2, y - 11, row[1], size=7)
        text_center(c, (apt_x[2]+apt_x[3])/2, y - 11, row[2], size=7)
        text_center(c, (apt_x[3]+apt_x[4])/2, y - 11, row[3], size=7)
        text_center(c, (apt_x[4]+apt_x[5])/2, y - 11, row[4], size=7)
        text_center(c, (apt_x[5]+apt_x[6])/2, y - 11, row[5], size=7)
        text_center(c, (apt_x[6]+apt_x[7])/2, y - 11, row[6], size=7)
        text_center(c, (apt_x[7]+apt_x[8])/2, y - 11, row[7], size=7)
        text_center(c, (apt_x[8]+apt_x[9])/2, y - 11, row[8], size=7)
        text_center(c, (apt_x[9]+apt_x[10])/2, y - 11, row[9], size=7)
        
        for idx in range(len(apt_x) - 1):
            c.line(apt_x[idx], y, apt_x[idx], y - row_h)
        y -= row_h


# ================= PAGE 3 (ATC PLAN & ENROUTE WINDS SUMMARY) =================

def page3(c, data=None):
    frame(c)
    
    text_center(c, W/2, 770, "ATC FLIGHT PLAN VOHS to VOCI", font="Courier-Bold", size=10)
    text_center(c, W/2, 758, "..........................................", font="Courier-Bold", size=10)
    
    y_atc = 735
    atc_strings = [
        "(FPL-VTKVR-IN",
        "-HA4T/M-SDFGHIRWXY/EB1",
        "-VOHS0730",
        "-N0469FL400 HIA Q21 BIA W118 CIA",
        "-VOCI0104 VOBL VOCB",
        "-PBN/A1B1C1D1O1S2 DOF/260701 REG/VTKVR OPR/TRANSWORLD JETS",
        "RMK/ TCAS EQUIPPED NO CREDIT FACILITY PIC VIVEK SONDHI MOB 9910561013 ALL INDIANS ON BOARD ENDURANCE 0430)"
    ]
    
    for line in atc_strings:
        text(c, 45, y_atc, line, size=8)
        y_atc -= 13
        
    y_winds = 625
    text_center(c, W/2, y_winds, "ENROUTE WINDS", font="Courier-Bold", size=9.5)
    
    w_cols = [45, 105, 160, 195, 250, 285, 340, 375, 430, 465, 520]
    
    y_winds -= 24
    text(c, w_cols[0], y_winds, "IDENT", font="Courier-Bold", size=8)
    text_center(c, (w_cols[1]+w_cols[2])/2, y_winds, "FL 340", font="Courier-Bold", size=8)
    text_center(c, (w_cols[3]+w_cols[4])/2, y_winds, "FL 360", font="Courier-Bold", size=8)
    text_center(c, (w_cols[5]+w_cols[6])/2, y_winds, "FL 380", font="Courier-Bold", size=8)
    text_center(c, (w_cols[7]+w_cols[8])/2, y_winds, "FL 400", font="Courier-Bold", size=8)
    text_center(c, (w_cols[9]+w_cols[10])/2, y_winds, "FL 430", font="Courier-Bold", size=8)
    
    y_winds -= 11
    text_center(c, (w_cols[1]+w_cols[2])/2, y_winds, "W/V", font="Courier-Bold", size=8)
    text(c, w_cols[2]+8, y_winds, "TMP", font="Courier-Bold", size=8)
    text_center(c, (w_cols[3]+w_cols[4])/2, y_winds, "W/V", font="Courier-Bold", size=8)
    text(c, w_cols[4]+8, y_winds, "TMP", font="Courier-Bold", size=8)
    text_center(c, (w_cols[5]+w_cols[6])/2, y_winds, "W/V", font="Courier-Bold", size=8)
    text(c, w_cols[6]+8, y_winds, "TMP", font="Courier-Bold", size=8)
    text_center(c, (w_cols[7]+w_cols[8])/2, y_winds, "W/V", font="Courier-Bold", size=8)
    text(c, w_cols[8]+8, y_winds, "TMP", font="Courier-Bold", size=8)
    text_center(c, (w_cols[9]+w_cols[10])/2, y_winds, "W/V", font="Courier-Bold", size=8)
    text(c, w_cols[10]+8, y_winds, "TMP", font="Courier-Bold", size=8)
    
    y_winds -= 14
    
    winds_matrix_data = [
        ("HIA", "060/019", "+17", "064/022", "+15", "068/025", "+9", "072/030", "+4", "076/038", "-4"),
        ("LURGI", "049/021", "+17", "058/022", "+15", "065/024", "+9", "072/027", "+4", "078/032", "-5"),
        ("PADBI", "077/021", "+17", "076/024", "+15", "075/027", "+9", "071/030", "+3", "064/036", "-5"),
        ("-TOC-", "080/021", "+17", "078/024", "+15", "076/027", "+9", "071/031", "+3", "063/037", "-5"),
        ("RITNU", "084/023", "+16", "080/026", "+14", "077/029", "+9", "071/033", "+3", "062/039", "-5"),
        ("TELUV", "080/026", "+16", "078/031", "+14", "076/036", "+8", "073/039", "+3", "070/042", "-5"),
        ("BIA", "070/030", "+16", "074/036", "+14", "077/042", "+8", "076/046", "+3", "072/050", "-5"),
        ("AKTIM", "063/030", "+16", "071/036", "+14", "076/043", "+8", "075/048", "+2", "070/055", "-6"),
        ("-TOD-", "066/026", "+15", "071/034", "+13", "075/042", "+8", "073/048", "+2", "070/056", "-6"),
        ("SATBI", "066/026", "+15", "072/034", "+13", "075/042", "+8", "073/048", "+2", "070/056", "-6"),
        ("CCB", "075/026", "+15", "074/034", "+13", "073/042", "+8", "071/048", "+2", "068/056", "-6"),
        ("CIA", "096/027", "+13", "080/036", "+12", "071/047", "+8", "069/053", "+3", "069/060", "-6"),
        ("CIA", "266/008", "+16", "297/004", "+17", "339/005", "+18", "343/010", "+18", "359/010", "+18"),
        ("-TOC-", "265/010", "+16", "287/009", "+17", "314/008", "+18", "333/008", "+18", "355/007", "+18"),
        ("CCB", "263/013", "+16", "284/012", "+17", "309/011", "+18", "326/008", "+19", "003/004", "+18"),
        ("LENBO", "271/013", "+16", "285/011", "+17", "306/009", "+18", "323/007", "+19", "006/004", "+18"),
        ("UGABA", "275/015", "+16", "281/011", "+17", "295/007", "+18", "315/005", "+19", "012/004", "+18"),
        ("-TOD-", "269/015", "+17", "272/011", "+17", "285/008", "+18", "297/005", "+19", "028/004", "+19"),
        ("BIA", "263/015", "+17", "264/012", "+17", "278/009", "+18", "289/005", "+19", "046/003", "+19"),
        ("CIA", "292/015", "+11", "292/018", "+12", "287/022", "+13", "280/023", "+14", "273/020", "+15"),
        ("-TOC-", "290/015", "+11", "291/018", "+12", "287/022", "+13", "280/023", "+14", "273/020", "+15"),
        ("-TOD-", "261/017", "+12", "275/020", "+13", "281/022", "+14", "279/021", "+15", "273/018", "+16"),
        ("CCB", "255/019", "+12", "269/021", "+14", "278/022", "+14", "278/021", "+15", "273/017", "+16")
    ]
    
    for row in winds_matrix_data:
        text(c, w_cols[0], y_winds, row[0], size=8)
        text_center(c, (w_cols[1]+w_cols[2])/2, y_winds, row[1], size=8)
        text(c, w_cols[2]+10, y_winds, row[2], size=8)
        text_center(c, (w_cols[3]+w_cols[4])/2, y_winds, row[3], size=8)
        text(c, w_cols[4]+10, y_winds, row[4], size=8)
        text_center(c, (w_cols[5]+w_cols[6])/2, y_winds, row[5], size=8)
        text(c, w_cols[6]+10, y_winds, row[6], size=8)
        text_center(c, (w_cols[7]+w_cols[8])/2, y_winds, row[7], size=8)
        text(c, w_cols[8]+10, y_winds, row[8], size=8)
        text_center(c, (w_cols[9]+w_cols[10])/2, y_winds, row[9], size=8)
        text(c, w_cols[10]+10, y_winds, row[10], size=8)
        y_winds -= 13.5

    text_center(c, W/2, 65, "************** END OF THE REPORT    **************", font="Courier-Bold", size=9)
    
    c.setLineWidth(0.5)
    c.line(45, 48, W-45, 48)
    text(c, 45, 38, "COMPUTED DATE : 01-07-2026", font="Courier-Bold", size=8)
    text_right(c, W-45, 38, "TIME : 05:48:38 UTC", font="Courier-Bold", size=8)


def build_pdf(data=None, output="Navlog.pdf"):
    c = canvas.Canvas(output, pagesize=A4)
    page1(c, data)
    c.showPage()
    page2(c, data)
    c.showPage()
    page3(c, data)
    c.showPage()
    c.save()
    print("PDF Generated Successfully")

if __name__ == "__main__":
    build_pdf()