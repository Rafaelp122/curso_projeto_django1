import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from recipes.models import Category, Recipe
from faker import Faker

User = get_user_model()


class Command(BaseCommand):
    help = 'Popula o banco de dados com receitas aleatórias'

    def add_arguments(self, parser):
        parser.add_argument(
            '--number',
            type=int,
            default=50,
            help='Número de receitas a serem criadas (padrão: 50)'
        )

    def handle(self, *args, **options):
        fake = Faker('pt_BR')
        number = options['number']

        # Criar usuário padrão se não existir
        user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'first_name': 'Admin',
                'last_name': 'User',
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if _:
            user.set_password('admin')
            user.save()

        # Criar categorias se não existirem
        categories_names = [
            'Café da Manhã', 'Almoço', 'Jantar', 'Sobremesas',
            'Lanches', 'Bebidas', 'Saladas', 'Massas',
            'Carnes', 'Peixes', 'Vegetariano', 'Vegano'
        ]
        categories = []
        for name in categories_names:
            category, _ = Category.objects.get_or_create(name=name)
            categories.append(category)

        # Unidades de tempo e porções
        time_units = ['minutos', 'horas']
        serving_units = ['porções', 'pessoas', 'unidades']

        # Criar receitas
        self.stdout.write(self.style.WARNING(f'Criando {number} receitas...'))
        
        created_count = 0
        for i in range(number):
            try:
                title = fake.sentence(nb_words=4).replace('.', '')
                
                recipe = Recipe.objects.create(
                    title=title,
                    description=fake.text(max_nb_chars=150),
                    preparation_time=random.randint(10, 180),
                    preparation_time_unit=random.choice(time_units),
                    servings=random.randint(1, 12),
                    servings_unit=random.choice(serving_units),
                    preparation_steps='\n'.join([
                        f'{j+1}. {fake.sentence()}' 
                        for j in range(random.randint(3, 8))
                    ]),
                    preparation_steps_is_html=False,
                    is_published=True,
                    category=random.choice(categories),
                    author=user,
                )
                created_count += 1
                
                if (i + 1) % 10 == 0:
                    self.stdout.write(
                        self.style.SUCCESS(f'{i + 1} receitas criadas...')
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Erro ao criar receita {i+1}: {str(e)}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ {created_count} receitas criadas com sucesso!'
            )
        )
