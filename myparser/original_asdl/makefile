gen: genC genH


genC:
	python asdl_c.py -c $(ASDL).c ../asdls/$(ASDL).asdl 

genH:
	python asdl_c.py -h $(ASDL).h ../asdls/$(ASDL).asdl
