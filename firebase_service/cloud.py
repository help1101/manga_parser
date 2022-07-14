import json
import threading
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_service.fb_credentials import Credentials


class CloudDb(Credentials):
    callback_done = threading.Event()
    delete_done = threading.Event()

    db = firestore.client()

    def add_popular(self, language: str, source: str, data):
        doc_ref = self.db.collection(u'catalogue').document(language).collection(source).document(source)
        doc_ref.set(data)

    def on_snapshot(self, doc_snapshot, changes, read_time):
        for doc in doc_snapshot:
            print(f'Received document snapshot: {doc.id}')

        for change in changes:
            if change.type.name == 'ADDED':
                print(f'Data added: {change.document.id}')
            elif change.type.name == 'MODIFIED':
                print(f'Data has been updated: {change.document.id}')
            elif change.type.name == 'DELETED':
                print(f'Data has been deleted: {change.document.id}')

        self.callback_done.set()

    def doc_subscribe(self):
        # doc_ref = self.db.collection(u'mangas').document(u'readmanga')
        doc_ref = self.db.collection(u'mangas').document(u'readmanga').collection(u'popular').document(u'popular')

        doc_watch = doc_ref.on_snapshot(self.on_snapshot)
        return doc_watch

    def update_catalogue(self, language: str, source: str, data):
        """
        :param language: language of source. Use language code like: en (document)
        :param source: the name of your source (collection)
        :param data: the data you need to add / update
        :return: None
        """

        doc_ref = self.db.collection(u'catalogue').document(language).collection(source).document(source)
        doc_ref.update(data)



# q = CloudDb()
# q.doc_subscribe()
# q.add_popular()
# q.update_popular()
# q.doc_subscribe().unsubscribe()
