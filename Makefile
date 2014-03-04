run:
	python shingles.py karenina1_utf.html karenina2_utf.html

run1:
	python shingles.py 1 2

run2:
	python shingles.py karenina1_utf_small karenina2_utf_small

clean:
	find . -name \*~ -delete
	find . -name \*.backup -delete

	find $(CDIR) -name \*~ -delete
	find $(CDIR) -name \*.backup -delete

