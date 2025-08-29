from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count, Avg
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Restaurant, MenuItem
from .forms import RestaurantForm, MenuItemForm

def is_admin_or_superuser(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)

@login_required
@user_passes_test(is_admin_or_superuser)
def add_restaurant(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            restaurant = form.save(commit=False)
            # For superuser, they can assign ownership to any user
            # For now, we'll set the current user as owner
            restaurant.owner = request.user
            restaurant.save()
            messages.success(request, f'Restaurant "{restaurant.name}" has been added successfully!')
            return redirect('restaurant:dashboard', pk=restaurant.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RestaurantForm()

    return render(request, 'restaurant/add_restaurant.html', {'form': form})

@login_required
def restaurant_dashboard(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)

    # Check if user has permission to access this dashboard
    if not (request.user.is_superuser or request.user.is_staff or restaurant.owner == request.user):
        messages.error(request, "You don't have permission to access this dashboard.")
        return redirect('users:home')

    # Get dashboard statistics
    menu_items = restaurant.menu_items.all()
    total_items = menu_items.count()
    available_items = menu_items.filter(is_available=True).count()
    vegetarian_items = menu_items.filter(is_vegetarian=True).count()

    # Get recent menu items
    recent_items = menu_items.order_by('-created_at')[:5]

    context = {
        'restaurant': restaurant,
        'total_items': total_items,
        'available_items': available_items,
        'vegetarian_items': vegetarian_items,
        'recent_items': recent_items,
    }

    return render(request, 'restaurant/dashboard.html', context)

@login_required
def my_restaurants(request):
    """View for restaurant owners to see their restaurants"""
    if request.user.is_superuser:
        restaurants = Restaurant.objects.all()
    else:
        restaurants = request.user.owned_restaurants.all()

    context = {
        'restaurants': restaurants,
        'is_owner_view': True,
    }

    return render(request, 'restaurant/my_restaurants.html', context)

@login_required
def manage_menu(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)

    # Check permissions
    if not (request.user.is_superuser or request.user.is_staff or restaurant.owner == request.user):
        messages.error(request, "You don't have permission to manage this menu.")
        return redirect('users:home')

    menu_items = restaurant.menu_items.all().order_by('category', 'name')

    # Handle search and filtering
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')

    if search_query:
        menu_items = menu_items.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    if category_filter:
        menu_items = menu_items.filter(category=category_filter)

    # Pagination
    paginator = Paginator(menu_items, 12)
    page_number = request.GET.get('page')
    menu_items = paginator.get_page(page_number)

    context = {
        'restaurant': restaurant,
        'menu_items': menu_items,
        'search_query': search_query,
        'category_filter': category_filter,
        'categories': MenuItem.CATEGORY_CHOICES,
    }

    return render(request, 'restaurant/manage_menu.html', context)

@login_required
def add_menu_item(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)

    # Check permissions
    if not (request.user.is_superuser or request.user.is_staff or restaurant.owner == request.user):
        messages.error(request, "You don't have permission to add menu items.")
        return redirect('users:home')

    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.restaurant = restaurant
            menu_item.save()
            messages.success(request, f'Menu item "{menu_item.name}" has been added successfully!')
            return redirect('restaurant:manage_menu', pk=restaurant.pk)
    else:
        form = MenuItemForm()

    context = {
        'form': form,
        'restaurant': restaurant,
    }

    return render(request, 'restaurant/add_menu_item.html', context)

class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurant/restaurant_list.html'
    context_object_name = 'restaurants'
    paginate_by = 12

    def get_queryset(self):
        queryset = Restaurant.objects.filter(status='active')
        search_query = self.request.GET.get('search', '')
        category_filter = self.request.GET.get('category', '')

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(address__icontains=search_query)
            )

        if category_filter:
            queryset = queryset.filter(category=category_filter)

        return queryset.order_by('-rating', '-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['category_filter'] = self.request.GET.get('category', '')
        context['categories'] = Restaurant.CATEGORY_CHOICES
        return context
