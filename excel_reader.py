import xlrd
from database import db
from database import Books,Students
db.create_all()
# how to delete entire table
# for i in range(1,len(Books.query.all())):
#     book=Books.query.get(i)
#     print(book)
#     db.session.delete(book)
#     db.session.commit()

wb = xlrd.open_workbook('home_book.xlsx')
sh = wb.sheet_by_index(0)
print( sh.cell_value(1,0) )
#3-7735
count=0
for i in range (3,7734):
    # row2 = sh.row(i)
    # if row2[1].find('empty'):
    # print( row2[1])
    if sh.cell_value(i, 1):
        print(f"{count}:{sh.cell_value(i, 1)}:   {sh.cell_value(i, 2)}")
        book = Books(book_topic=sh.cell_value(i, 1).strip(), book_code=sh.cell_value(i, 2).strip())
        db.session.add(book)
        db.session.commit()
    count=count+1



