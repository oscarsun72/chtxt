#!/bin/bash

DOC2TXT="/usr/local/bin/doc2txt,pl"
DOCX2TXT="/usr/local/bin/docx2txt"
EPUB2TXT="/usr/local/bin/epub2txt"
AZW2EPUB="/usr/local/bin/convert-ebook-osx"

FILE="$1"

case "$FILE" in

  *.doc)
	if [ ! -x $DOC2TXT ]; then
    	echo "$DOC2TXT NOT FOUND"
	else
	    $DOC2TXT "$FILE"	
	fi
    ;;

  *.docx)
	# pip3 install docx2txt
	NAME=$(echo $FILE|perl -pe 's/\.docx//g')
	if [ ! -x $DOCX2TXT ]; then
    	echo "$DOCX2TXT NOT FOUND"
	else
	    $DOCX2TXT "$FILE" > "${NAME}.txt"	
		if [ $? -eq 0 ]; then
			echo "Done. ${NAME}.txt"
		fi
	fi
    ;;

  *.epub)
	# https://github.com/kevinboone/epub2txt2
	NAME=$(echo $FILE|perl -pe 's/\.epub//g')
	if [ ! -x $EPUB2TXT ]; then
    	echo "$EPUB2TXT NOT FOUND"
	else
	    $EPUB2TXT -n "${NAME}.epub" > "${NAME}.txt"	
		if [ $? -eq 0 ]; then
			echo "Done. ${NAME}.txt"
		fi
	fi
    ;;

  *.azw3)
	# https://github.com/jianyun8023/convert-ebook
	if [ ! -x $AZW2EPUB ]; then
    	echo "$AZW2TXT NOT FOUND"
	else
	    $AZW2EPUB "$FILE"	
	fi

	EPUB_NAME=$(echo $FILE|perl -pe 's/\.azw3//g')

	if [ ! -x $EPUB2TXT ]; then
    	echo "$EPUB2TXT NOT FOUND"
	else
	    $EPUB2TXT -n "${EPUB_NAME}.epub" > "${EPUB_NAME}.txt" 	
	fi

    ;;

  *)
    echo "Usage: $0 <ebook_file:.doc,.docx,.epub,.azw3>" 
    ;;
esac
