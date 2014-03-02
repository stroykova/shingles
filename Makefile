run:
	python script.py karenina1_utf.html karenina2_utf.html
clean:
	find . -name \*~ -delete
	find . -name \*.backup -delete

	find $(CDIR) -name \*~ -delete
	find $(CDIR) -name \*.backup -delete

