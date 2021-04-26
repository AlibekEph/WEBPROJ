class Member(db.Model):
	__tablename__ = 'members'
	id = db.Column(db.Integer, primary_key=True)
	scores = db.Column(db.Integer, nullable=False)
	mark = db.Column(db.String(250), nullable=False)
	name = db.Column(db.String(250), nullable=False)