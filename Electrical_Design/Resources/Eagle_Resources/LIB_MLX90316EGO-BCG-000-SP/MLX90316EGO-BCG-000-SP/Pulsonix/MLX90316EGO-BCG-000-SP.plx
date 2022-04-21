PULSONIX_LIBRARY_ASCII "SamacSys ECAD Model"
//883812/829533/2.49/16/3/Integrated Circuit

(asciiHeader
	(fileUnits MM)
)
(library Library_1
	(padStyleDef "r145_45"
		(holeDiam 0)
		(padShape (layerNumRef 1) (padShapeType Rect)  (shapeWidth 0.45) (shapeHeight 1.45))
		(padShape (layerNumRef 16) (padShapeType Ellipse)  (shapeWidth 0) (shapeHeight 0))
	)
	(textStyleDef "Normal"
		(font
			(fontType Stroke)
			(fontFace "Helvetica")
			(fontHeight 1.27)
			(strokeWidth 0.127)
		)
	)
	(patternDef "SOP65P640X110-16N" (originalName "SOP65P640X110-16N")
		(multiLayer
			(pad (padNum 1) (padStyleRef r145_45) (pt -2.925, 2.275) (rotation 90))
			(pad (padNum 2) (padStyleRef r145_45) (pt -2.925, 1.625) (rotation 90))
			(pad (padNum 3) (padStyleRef r145_45) (pt -2.925, 0.975) (rotation 90))
			(pad (padNum 4) (padStyleRef r145_45) (pt -2.925, 0.325) (rotation 90))
			(pad (padNum 5) (padStyleRef r145_45) (pt -2.925, -0.325) (rotation 90))
			(pad (padNum 6) (padStyleRef r145_45) (pt -2.925, -0.975) (rotation 90))
			(pad (padNum 7) (padStyleRef r145_45) (pt -2.925, -1.625) (rotation 90))
			(pad (padNum 8) (padStyleRef r145_45) (pt -2.925, -2.275) (rotation 90))
			(pad (padNum 9) (padStyleRef r145_45) (pt 2.925, -2.275) (rotation 90))
			(pad (padNum 10) (padStyleRef r145_45) (pt 2.925, -1.625) (rotation 90))
			(pad (padNum 11) (padStyleRef r145_45) (pt 2.925, -0.975) (rotation 90))
			(pad (padNum 12) (padStyleRef r145_45) (pt 2.925, -0.325) (rotation 90))
			(pad (padNum 13) (padStyleRef r145_45) (pt 2.925, 0.325) (rotation 90))
			(pad (padNum 14) (padStyleRef r145_45) (pt 2.925, 0.975) (rotation 90))
			(pad (padNum 15) (padStyleRef r145_45) (pt 2.925, 1.625) (rotation 90))
			(pad (padNum 16) (padStyleRef r145_45) (pt 2.925, 2.275) (rotation 90))
		)
		(layerContents (layerNumRef 18)
			(attr "RefDes" "RefDes" (pt 0, 0) (textStyleRef "Normal") (isVisible True))
		)
		(layerContents (layerNumRef Courtyard_Top)
			(line (pt -3.9 2.8) (pt 3.9 2.8) (width 0.05))
		)
		(layerContents (layerNumRef Courtyard_Top)
			(line (pt 3.9 2.8) (pt 3.9 -2.8) (width 0.05))
		)
		(layerContents (layerNumRef Courtyard_Top)
			(line (pt 3.9 -2.8) (pt -3.9 -2.8) (width 0.05))
		)
		(layerContents (layerNumRef Courtyard_Top)
			(line (pt -3.9 -2.8) (pt -3.9 2.8) (width 0.05))
		)
		(layerContents (layerNumRef 28)
			(line (pt -2.2 2.5) (pt 2.2 2.5) (width 0.025))
		)
		(layerContents (layerNumRef 28)
			(line (pt 2.2 2.5) (pt 2.2 -2.5) (width 0.025))
		)
		(layerContents (layerNumRef 28)
			(line (pt 2.2 -2.5) (pt -2.2 -2.5) (width 0.025))
		)
		(layerContents (layerNumRef 28)
			(line (pt -2.2 -2.5) (pt -2.2 2.5) (width 0.025))
		)
		(layerContents (layerNumRef 28)
			(line (pt -2.2 1.85) (pt -1.55 2.5) (width 0.025))
		)
		(layerContents (layerNumRef 18)
			(line (pt -1.85 2.5) (pt 1.85 2.5) (width 0.2))
		)
		(layerContents (layerNumRef 18)
			(line (pt 1.85 2.5) (pt 1.85 -2.5) (width 0.2))
		)
		(layerContents (layerNumRef 18)
			(line (pt 1.85 -2.5) (pt -1.85 -2.5) (width 0.2))
		)
		(layerContents (layerNumRef 18)
			(line (pt -1.85 -2.5) (pt -1.85 2.5) (width 0.2))
		)
		(layerContents (layerNumRef 18)
			(line (pt -3.65 2.85) (pt -2.2 2.85) (width 0.2))
		)
	)
	(symbolDef "MLX90316EGO-BCG-000-SP" (originalName "MLX90316EGO-BCG-000-SP")

		(pin (pinNum 1) (pt 0 mils 0 mils) (rotation 0) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 230 mils -25 mils) (rotation 0]) (justify "Left") (textStyleRef "Normal"))
		))
		(pin (pinNum 2) (pt 0 mils -100 mils) (rotation 0) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 230 mils -125 mils) (rotation 0]) (justify "Left") (textStyleRef "Normal"))
		))
		(pin (pinNum 3) (pt 0 mils -200 mils) (rotation 0) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 230 mils -225 mils) (rotation 0]) (justify "Left") (textStyleRef "Normal"))
		))
		(pin (pinNum 4) (pt 0 mils -300 mils) (rotation 0) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 230 mils -325 mils) (rotation 0]) (justify "Left") (textStyleRef "Normal"))
		))
		(pin (pinNum 5) (pt 0 mils -400 mils) (rotation 0) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 230 mils -425 mils) (rotation 0]) (justify "Left") (textStyleRef "Normal"))
		))
		(pin (pinNum 6) (pt 0 mils -500 mils) (rotation 0) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 230 mils -525 mils) (rotation 0]) (justify "Left") (textStyleRef "Normal"))
		))
		(pin (pinNum 7) (pt 0 mils -600 mils) (rotation 0) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 230 mils -625 mils) (rotation 0]) (justify "Left") (textStyleRef "Normal"))
		))
		(pin (pinNum 8) (pt 0 mils -700 mils) (rotation 0) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 230 mils -725 mils) (rotation 0]) (justify "Left") (textStyleRef "Normal"))
		))
		(pin (pinNum 9) (pt 2200 mils 0 mils) (rotation 180) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 1970 mils -25 mils) (rotation 0]) (justify "Right") (textStyleRef "Normal"))
		))
		(pin (pinNum 10) (pt 2200 mils -100 mils) (rotation 180) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 1970 mils -125 mils) (rotation 0]) (justify "Right") (textStyleRef "Normal"))
		))
		(pin (pinNum 11) (pt 2200 mils -200 mils) (rotation 180) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 1970 mils -225 mils) (rotation 0]) (justify "Right") (textStyleRef "Normal"))
		))
		(pin (pinNum 12) (pt 2200 mils -300 mils) (rotation 180) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 1970 mils -325 mils) (rotation 0]) (justify "Right") (textStyleRef "Normal"))
		))
		(pin (pinNum 13) (pt 2200 mils -400 mils) (rotation 180) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 1970 mils -425 mils) (rotation 0]) (justify "Right") (textStyleRef "Normal"))
		))
		(pin (pinNum 14) (pt 2200 mils -500 mils) (rotation 180) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 1970 mils -525 mils) (rotation 0]) (justify "Right") (textStyleRef "Normal"))
		))
		(pin (pinNum 15) (pt 2200 mils -600 mils) (rotation 180) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 1970 mils -625 mils) (rotation 0]) (justify "Right") (textStyleRef "Normal"))
		))
		(pin (pinNum 16) (pt 2200 mils -700 mils) (rotation 180) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 1970 mils -725 mils) (rotation 0]) (justify "Right") (textStyleRef "Normal"))
		))
		(line (pt 200 mils 100 mils) (pt 2000 mils 100 mils) (width 6 mils))
		(line (pt 2000 mils 100 mils) (pt 2000 mils -800 mils) (width 6 mils))
		(line (pt 2000 mils -800 mils) (pt 200 mils -800 mils) (width 6 mils))
		(line (pt 200 mils -800 mils) (pt 200 mils 100 mils) (width 6 mils))
		(attr "RefDes" "RefDes" (pt 2050 mils 300 mils) (justify Left) (isVisible True) (textStyleRef "Normal"))
		(attr "Type" "Type" (pt 2050 mils 200 mils) (justify Left) (isVisible True) (textStyleRef "Normal"))

	)
	(compDef "MLX90316EGO-BCG-000-SP" (originalName "MLX90316EGO-BCG-000-SP") (compHeader (numPins 16) (numParts 1) (refDesPrefix IC)
		)
		(compPin "1" (pinName "VDIG1") (partNum 1) (symPinNum 1) (gateEq 0) (pinEq 0) (pinType Unknown))
		(compPin "2" (pinName "VSS1") (partNum 1) (symPinNum 2) (gateEq 0) (pinEq 0) (pinType Unknown))
		(compPin "3" (pinName "VDD1") (partNum 1) (symPinNum 3) (gateEq 0) (pinEq 0) (pinType Unknown))
		(compPin "4" (pinName "TEST 01") (partNum 1) (symPinNum 4) (gateEq 0) (pinEq 0) (pinType Unknown))
		(compPin "5" (pinName "__SS2__/SWITCH2") (partNum 1) (symPinNum 5) (gateEq 0) (pinEq 0) (pinType Unknown))
		(compPin "6" (pinName "SCLK2") (partNum 1) (symPinNum 6) (gateEq 0) (pinEq 0) (pinType Unknown))
		(compPin "7" (pinName "OUT2/MOSI/MISO2") (partNum 1) (symPinNum 7) (gateEq 0) (pinEq 0) (pinType Unknown))
		(compPin "8" (pinName "TEST 12") (partNum 1) (symPinNum 8) (gateEq 0) (pinEq 0) (pinType Unknown))
		(compPin "16" (pinName "TEST 11") (partNum 1) (symPinNum 9) (gateEq 0) (pinEq 0) (pinType Unknown))
		(compPin "15" (pinName "OUT1/MOSI/MISO1") (partNum 1) (symPinNum 10) (gateEq 0) (pinEq 0) (pinType Unknown))
		(compPin "14" (pinName "SCLK1") (partNum 1) (symPinNum 11) (gateEq 0) (pinEq 0) (pinType Unknown))
		(compPin "13" (pinName "__SS1__/SWITCH1") (partNum 1) (symPinNum 12) (gateEq 0) (pinEq 0) (pinType Unknown))
		(compPin "12" (pinName "TEST 02") (partNum 1) (symPinNum 13) (gateEq 0) (pinEq 0) (pinType Unknown))
		(compPin "11" (pinName "VDD2") (partNum 1) (symPinNum 14) (gateEq 0) (pinEq 0) (pinType Unknown))
		(compPin "10" (pinName "VSS2") (partNum 1) (symPinNum 15) (gateEq 0) (pinEq 0) (pinType Unknown))
		(compPin "9" (pinName "VDIG2") (partNum 1) (symPinNum 16) (gateEq 0) (pinEq 0) (pinType Unknown))
		(attachedSymbol (partNum 1) (altType Normal) (symbolName "MLX90316EGO-BCG-000-SP"))
		(attachedPattern (patternNum 1) (patternName "SOP65P640X110-16N")
			(numPads 16)
			(padPinMap
				(padNum 1) (compPinRef "1")
				(padNum 2) (compPinRef "2")
				(padNum 3) (compPinRef "3")
				(padNum 4) (compPinRef "4")
				(padNum 5) (compPinRef "5")
				(padNum 6) (compPinRef "6")
				(padNum 7) (compPinRef "7")
				(padNum 8) (compPinRef "8")
				(padNum 9) (compPinRef "9")
				(padNum 10) (compPinRef "10")
				(padNum 11) (compPinRef "11")
				(padNum 12) (compPinRef "12")
				(padNum 13) (compPinRef "13")
				(padNum 14) (compPinRef "14")
				(padNum 15) (compPinRef "15")
				(padNum 16) (compPinRef "16")
			)
		)
		(attr "Mouser Part Number" "482-90316EGOBCG000SP")
		(attr "Mouser Price/Stock" "https://www.mouser.co.uk/ProductDetail/Melexis/MLX90316EGO-BCG-000-SP?qs=KuGPmAKtFKWg%2F1YUwHrLHw%3D%3D")
		(attr "Manufacturer_Name" "Melexis")
		(attr "Manufacturer_Part_Number" "MLX90316EGO-BCG-000-SP")
		(attr "Description" "Board Mount Motion & Position Sensors Triaxis Programmable Rotary Position Sensor feat. Ana-PWM")
		(attr "<Hyperlink>" "https://www.melexis.com/-/media/files/documents/datasheets/mlx90316-datasheet-melexis.pdf")
		(attr "<Component Height>" "1.1")
		(attr "<STEP Filename>" "MLX90316EGO-BCG-000-SP.stp")
		(attr "<STEP Offsets>" "X=0;Y=0;Z=0")
		(attr "<STEP Rotation>" "X=0;Y=0;Z=0")
	)

)
