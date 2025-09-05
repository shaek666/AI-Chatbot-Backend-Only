from django.core.management.base import BaseCommand
from rag.services import rag_service
import os

class Command(BaseCommand):
    help = 'Populates the Pinecone index with documents from a specified directory.'

    def add_arguments(self, parser):
        parser.add_argument('docs_dir', type=str, help='The directory containing documents to index.')

    def handle(self, *args, **options):
        docs_dir = options['docs_dir']
        if not os.path.isdir(docs_dir):
            self.stderr.write(self.style.ERROR(f'Error: Directory "{docs_dir}" not found.'))
            return

        self.stdout.write(self.style.SUCCESS(f'Starting to index documents from: {docs_dir}'))

        if not rag_service or not rag_service.pinecone_available:
            self.stderr.write(self.style.ERROR('RAG service or Pinecone not available. Cannot populate index.'))
            return

        for filename in os.listdir(docs_dir):
            filepath = os.path.join(docs_dir, filename)
            if os.path.isfile(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    doc_id = os.path.splitext(filename)[0] # Use filename without extension as doc_id
                    title = filename # Use filename as title
                    
                    if rag_service.add_document(doc_id, title, content):
                        self.stdout.write(self.style.SUCCESS(f'Successfully added {filename} to index.'))
                    else:
                        self.stderr.write(self.style.ERROR(f'Failed to add {filename} to index.'))
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f'Error processing {filename}: {e}'))
        
        self.stdout.write(self.style.SUCCESS('Document indexing complete.'))