from flask import render_template,request,redirect,make_response,flash,jsonify
from database import db
from database import app
from database import Librarian,Students,Books,borrow,Borrow_history
import jdatetime
db.create_all()
@app.route("/borrow_book",methods=['POST','GET'])
def borrow_book():
    if request.cookies.get("user"):
        if request.method=='POST':
            book_topic=""
            student_name=""
            book_code = request.form.get('book_code')
            student_number = request.form.get('student_number')
            student_book_count=0
            for brr in borrow.query.all():
                if student_number==brr.student_number:
                    student_book_count+=1
            found = False
            borrow_check=False
            for book in Books.query.all():
                if book_code == book.book_code:
                    book_topic = book.book_topic

            for student in Students.query.all():
                if student_number == student.student_number:
                    student_name = student.student_name
                    student_family = student.student_family
                    student_book_count += 1
            for brr in borrow.query.all():
                if book_code==brr.book_code:
                    borrow_check=True
                    flash("کتاب اکنون در امانت شخص دیگری است", "danger")
                    return redirect('/borrow_book')
            if student_book_count>3:
                flash("تعداد کتاب های به امانت گرفته شده توسط دانش آموز بیشتر از حد مجاز است", "danger")
                return redirect('/borrow_book')


            if book_topic and student_name and not borrow_check and student_book_count<4:
                found=True
                bor=borrow(book_topic=book_topic,book_code=book_code,student_name=student_name,student_family=student_family,student_number=student_number,first_date_of_borrow=jdatetime.datetime.now().strftime("%Y/%m/%d"),second_date_of_borrow=jdatetime.datetime.now().strftime("%Y/%m/%d"),number_of_extention=0,librarian=request.cookies.get("user"))
                db.session.add(bor)
                db.session.commit()
                flash("امانت با موفقیت ثبت شد", "success")
                return redirect('/')

            if not found:
                flash("شناسه کتاب یا شماره دانش آموزی نا درست است","danger")
                return redirect('/borrow_book')


        else:
            return render_template('borrow_book.html',user=request.cookies.get("user"))
    else:
        return redirect('/login')
@app.route("/add_book",methods=['POST','GET'])
def add_book():
    if request.cookies.get("user"):
        if request.method=='POST':
            book_topic = request.form.get('book_topic')
            book_code = request.form.get('book_code')
            found = False
            for book in Books.query.all():
                if book_code == book.book_code:
                    found = True
            if not found:
                book=Books(book_topic=book_topic,book_code=book_code)
                db.session.add(book)
                db.session.commit()
                flash("کتاب با موفقیت اضافه شد", "primary")
                return redirect('/')
            else:
                flash("کتاب با این شماره شناسایی وجود دارد", "danger")
                return redirect('/add_book')

        else:
            return render_template('add_book.html',user=request.cookies.get("user"))
    else:
        return redirect('/login')

@app.route("/add_student",methods=['POST','GET'])
def add_student():
    if request.cookies.get("user"):
        if request.method=='POST':
            student_name = request.form.get('student_name')
            student_family = request.form.get('student_family')
            student_id_code = request.form.get('student_id_code')
            student_number = request.form.get('student_number')
            student_phone = request.form.get('student_phone')
            student_parent_phone = request.form.get('student_parent_phone')
            home_phone = request.form.get('home_phone')
            found=False
            for student in Students.query.all():
                if student_number== student.student_number or student_id_code==student.student_id_code:
                    found=True
            if not found:
                student=Students(student_name=student_name,student_family=student_family,student_id_code=student_id_code,student_number=student_number,student_phone=student_phone,student_parent_phone=student_parent_phone,home_phone=home_phone)
                db.session.add(student)
                db.session.commit()
                flash("دانش آموز با موفقیت اضافه شد", "primary")
                return redirect('/')
            else:
                flash("دانش آموز با این شماره دانش آموزی یا کد ملی وجود دارد", "danger")
                return redirect('/add_student')

        else:
            return render_template('add_student.html',user=request.cookies.get("user"))
    else:
        return redirect('/login')

@app.route("/")
def home():
        return render_template('index.html',user=request.cookies.get("user"))
@app.route("/about")
def about():
        return render_template('about.html')

@app.route("/logout")
def logout():
    flash("کتابدار محترم خدانگهدار","danger")
    response = make_response(redirect('/login'))
    response.delete_cookie("user")
    return response
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        user = request.form.get('user')
        pas = request.form.get('pas')
        found=False
        for u in range(len(Librarian.query.all())):
            if user==Librarian.query.all()[u].username and pas==Librarian.query.all()[u].password:
                flash("کتابدار گرامی خوش آمدید","success")
                response=make_response(redirect('/'))
                response.set_cookie("user",user)
                found = True
                return response
        if found==False:
                flash("کتابدار یافت نشد", "danger")
                return render_template('login.html')
    return render_template('login.html')
@app.route('/register',methods=['POST','GET'])
def Register():
    if request.method=='POST':
        user_name1 = request.form.get('user')
        password1 = request.form.get('pas')
        re_password = request.form.get('pass')
        admin_pass = request.form.get('admin_pass')
        if admin_pass=="@s@di.saveh1818":
            if password1==re_password:
                admin1=Librarian(username=user_name1,password=password1)
                db.session.add(admin1)
                db.session.commit()
                flash("کتابدار با موفقیت اضافه شد","success")
                return redirect('/login')
            else:
                flash("رمز عبور با تکرار آن همخوانی ندارد","danger")
                return render_template('Register.html')
        else:
            flash("رمز مدیریت نا درست است", "danger")
            return redirect('/register')
    else:
        return render_template('Register.html')

@app.route("/book_list",methods=['POST','GET'])
def book_list():
    if request.cookies.get("user"):
            return render_template('book_list.html',user=request.cookies.get("user"),books=Books.query.all(),items=len(Books.query.all()),borrow=borrow.query.all())

@app.route("/student_list",methods=['POST','GET'])
def student_list():
    if request.cookies.get("user"):
            return render_template('student_list.html',user=request.cookies.get("user"),students=Students.query.all(),items=len(Students.query.all()))

@app.route("/borrow_list",methods=['POST','GET'])
def borrow_list():
    if request.cookies.get("user"):
            return render_template('borrow_list.html',user=request.cookies.get("user"),borrows=borrow.query.all(),items=len(borrow.query.all()),time_now=jdatetime.datetime.now().date(),jdatetime=jdatetime)

@app.route("/get_book_and_student",methods=['POST','GET'])
def get_book_and_student():
    # if request.cookies.get("user"):
        student_found=False
        book_found=False
        if request.method == 'POST':
            student_number = request.form.get('student_number')
            book_code = request.form.get('book_code')
            for student in Students.query.all():
                if student_number == student.student_number:
                    student_found = True
                    sudent_total=student.student_name+" "+student.student_family
                    # return jsonify(student=student.student_name+" "+student.student_family)
            if not student_found:
                sudent_total="دانش آموز پیدا نشد"
                # return jsonify(student="دانش آموز پیدا نشد")
            for book in Books.query.all():
                if book_code == book.book_code:
                    book_found = True
                    book_total=book.book_topic
                    # return jsonify(book=Books.book_topic)
            if not book_found:
                book_total="کتاب پیدا نشد"
                # return jsonify(book="کتاب پیدا نشد")
            return jsonify(student=sudent_total,book=book_total)
@app.route("/get_book",methods=['POST','GET'])
def get_book():
    # if request.cookies.get("user"):
        book_found=False
        if request.method == 'POST':
            book_search = request.form.get('book_search')
            for book in Books.query.all():
                if book.book_code.find(book_search) > -1 or book.book_topic.find(book_search) > -1:
                    book_found = True
                    book_id=book.id
                    book_total=book.book_topic
                    code=book.book_code
                    # return jsonify(book=Books.book_topic)
            if not book_found:
                book_id = ""
                code = ""
                book_total="کتاب پیدا نشد"
                # return jsonify(book="کتاب پیدا نشد")
            return jsonify(id=book_id,book=book_total,book_code=code)

# this is an API for future that people can search in library database using it
@app.route("/get_book_API",methods=['POST'])
def get_book_API():

        book_found=False
        book_search_topic_list = []
        book_search_code_list=[]
        if request.method == 'POST':
            book_search = request.get_json('book_search')
            book_search=book_search['book_search']
            print(book_search)
            for book in Books.query.all():
                if   book.book_code.find( book_search)>-1 or book.book_topic.find( book_search)>-1:
                    book_found = True
                    print(book.book_topic)
                    book_search_topic_list.append(book.book_topic)
                    book_search_code_list.append(book.book_code)
            if not book_found:
                book_code = ""
                book_topic="کتاب پیدا نشد"
            return jsonify(book_topic=book_search_topic_list,book_code=book_search_code_list)

@app.route("/get_student",methods=['POST','GET'])
def get_student():
    # if request.cookies.get("user"):
        student_found=False
        if request.method == 'POST':
            student_search = request.form.get('student_search')
            for student in Students.query.all():
                if student_search == student.student_number or student_search==student.student_name+" "+student.student_family:
                    student_found = True
                    student_id=student.id
                    student_total=student.student_name+ " " +student.student_family
                    code=student.student_number
                    student_phone=student.student_phone
                    student_parent_phone = student.student_parent_phone
                    home_phone = student.home_phone
                    # return jsonify(book=Books.book_topic)
            if not student_found:
                student_id = ""
                code = ""
                student_phone =""
                student_parent_phone = ""
                home_phone =""
                student_total="دانش آموز پیدا نشد"
                # return jsonify(book="کتاب پیدا نشد")
            return jsonify(id=student_id,student=student_total,student_code=code,student_phone=student_phone,student_parent_phone=student_parent_phone,home_phone=home_phone)

@app.route("/delete_borrow/<int:borrow_id>",methods=['POST','GET'])
def delete_borrow(borrow_id):
    if request.cookies.get("user"):
         borrow_D=borrow.query.get(borrow_id)
         borrow_hist=Borrow_history(book_topic=borrow_D.book_topic,book_code =borrow_D.book_code,student_name=borrow_D.student_name,student_family=borrow_D.student_family,student_number=borrow_D.student_number,date_of_borrow=borrow_D.first_date_of_borrow,date_of_back=jdatetime.datetime.now().strftime("%Y/%m/%d"),number_of_extention=borrow_D.number_of_extention,librarian=borrow_D.librarian)
         db.session.add(borrow_hist)
         db.session.commit()
         db.session.delete(borrow_D)
         db.session.commit()
         return redirect("/borrow_list")
    else:
        return redirect('/login')
@app.route("/refresh_borrow/<int:borrow_id>",methods=['POST','GET'])
def refresh_borrow(borrow_id):
    if request.cookies.get("user"):
         borrow_R=borrow.query.get(borrow_id)
         if borrow_R.number_of_extention<1:
            borrow_R.number_of_extention=borrow_R.number_of_extention+1
            borrow_R.second_date_of_borrow=jdatetime.datetime.now().strftime("%Y/%m/%d")
            db.session.commit()
            flash("کتاب با موفقیت تمدید شد","success")
            return redirect("/borrow_list")
         else:
            flash("تعداد تمدید ها بیشتر از حد مجاز است!کتاب باید بازگردانده شود", "danger")
            return redirect("/borrow_list")
    else:
        return redirect('/login')
@app.route("/delete_book/<int:book_id>",methods=['POST','GET'])
def delete_book(book_id):
    if request.cookies.get("user"):
         book=Books.query.get(book_id)
         db.session.delete(book)
         db.session.commit()
         return redirect("/book_list")
    else:
        return redirect('/login')
@app.route("/delete_student/<int:student_id>",methods=['POST','GET'])
def delete_student(student_id):
    if request.cookies.get("user"):
         student=Students.query.get(student_id)
         db.session.delete(student)
         db.session.commit()
         return redirect("/student_list")
    else:
        return redirect('/login')
@app.route("/student_edit/<int:student_id>",methods=['POST','GET'])
def student_edit(student_id):
    if request.cookies.get("user"):
        student = Students.query.get(student_id)
        if request.method == 'GET':
            return render_template('student_edit.html', student=student)
        if request.method == 'POST':
            student_name = request.form.get('student_name')
            student_family = request.form.get('student_family')
            student_id_code = request.form.get('student_id_code')
            student_number = request.form.get('student_number')
            student_phone = request.form.get('student_phone')
            student_parent_phone = request.form.get('student_parent_phone')
            home_phone = request.form.get('home_phone')
            student.student_name=student_name
            student.student_family = student_family
            student.student_id_code = student_id_code
            student.student_number = student_number
            student.student_phone = student_phone
            student.student_parent_phone = student_parent_phone
            student.home_phone = home_phone
            db.session.commit()
            flash("دانش آموز با موفقیت ویرایش شد", "primary")
            return redirect('/student_list')
    else:
        return redirect('/login')
@app.route("/student_details/<int:student_id>",methods=['POST','GET'])
def student_details(student_id):
    if request.cookies.get("user"):
        student = Students.query.get(student_id)
        brr_list=[]
        book_history_list = []
        for brr in borrow.query.all():
            if student.student_number==brr.student_number:
                brr_list.append(brr)
        for brr in Borrow_history.query.all():
            if student.student_number == brr.student_number:
                book_history_list.append(brr)
        return render_template('student_details.html',user=request.cookies.get("user"),book_history_list=book_history_list ,borrow_list=brr_list,time_now=jdatetime.datetime.now().date(),jdatetime=jdatetime)
@app.route("/book_details/<book_code>",methods=['POST','GET'])
def book_details(book_code):
    if request.cookies.get("user"):
        brr_list = []
        book_history_list=[]
        for brr in borrow.query.all():
            if book_code==brr.book_code:
                brr_list.append(brr)
        for brr in Borrow_history.query.all():
            if book_code==brr.book_code:
                book_history_list.append(brr)
        print(book_history_list)
        return render_template('book_details.html',user=request.cookies.get("user"),borrow_list=brr_list, book_history_list=book_history_list,time_now=jdatetime.datetime.now().date(),jdatetime=jdatetime)


@app.route("/book_edit/<int:book_id>",methods=['POST','GET'])
def book_edit(book_id):
    if request.cookies.get("user"):
        book = Books.query.get(book_id)
        if request.method == 'GET':
            return render_template('book_edit.html', book=book)
        if request.method == 'POST':
            book_topic = request.form.get('book_topic')
            book_code = request.form.get('book_code')
            book.book_topic = book_topic
            book.book_code = book_code

            db.session.commit()
            flash("کتاب با موفقیت ویرایش شد", "primary")
            return redirect('/book_list')
    else:
        return redirect('/login')

if __name__=='__main__':
    app.run(host='0.0.0.0',port=80, threaded=True)
