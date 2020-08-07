from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime, timedelta


Base = declarative_base()

class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=date.today())

    def __repr__(self):
        return self.task

class ToDo():
    def __init__(self):
        self.engine = create_engine('sqlite:///todo.db?check_same_thread=False')
        self.session = sessionmaker(bind=self.engine)()
        Base.metadata.create_all(self.engine)

    def list_tasks(self, days):
        today = datetime.today()
        for d in range(days):
            day = today + timedelta(days=d)
            day = day.date()
            day_date = day.strftime('%A %d %b')
            print(f'\n{day_date}:')
            rows = self.session.query(Table).filter(Table.deadline == day).order_by(Table.deadline).all()
            if not rows:
                print('Nothing to do!')
            for row in rows:
                print(row)
            print()

    def list_all_tasks(self):
        rows = self.session.query(Table).order_by(Table.deadline).all()
        if not rows:
            print('Nothing to do!')
        for i, row in enumerate(rows):
            print(f'{i + 1}. {row.task}. {row.deadline.strftime("%-d %b")}')
        print()

    def list_missed_tasks(self):
        today = datetime.today().date()
        rows = self.session.query(Table).filter(Table.deadline < today).order_by(Table.deadline).all()
        if not rows:
            print('Nothing is missed!')
        for i, row in enumerate(rows):
            print(f'{i + 1}. {row.task}. {row.deadline.strftime("%-d %b")}')
        print()

    def task_add(self):
        print('Enter task')
        task = input()
        print('Enter deadline')
        deadline = input()
        deadline = datetime.strptime(deadline, '%Y-%m-%d').date()
        new_row = Table(task=task, deadline=deadline)
        self.session.add(new_row)
        self.session.commit()
        print('The task has been added!')

    def task_del(self):
        print('Choose the number of the task you want to delete:')
        rows = self.session.query(Table).order_by(Table.deadline).all()
        for i, row in enumerate(rows):
            print(f'{i + 1}. {row.task}. {row.deadline.strftime("%-d %b")}')
        row_to_del = int(input()) - 1
        self.session.delete(rows[row_to_del])
        self.session.commit()
        print('The task has been deleted!')

    def run(self):
        while True:
            print('1) Today\'s tasks')
            print('2) Week\'s tasks')
            print('3) All tasks')
            print('4) Missed tasks')
            print('5) Add task')
            print('6) Delete task')
            print('0) Exit')
            command = input()
            if command == '1':
                self.list_tasks(1)
            elif command == '2':
                self.list_tasks(7)
            elif command == '3':
                self.list_all_tasks()
            elif command == '4':
                self.list_missed_tasks()
            elif command == '5':
                self.task_add()
            elif command == '6':
                self.task_del()
            elif command == '0':
                print('Bye!')
                exit()


app = ToDo()
app.run()
