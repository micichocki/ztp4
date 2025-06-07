from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from app.viewmodels.product_viewmodel import ProductViewModel
from app.services.product_service import ProductService

class ProductListScreen(MDScreen):
    def __init__(self, view_model: ProductViewModel, **kwargs):
        super().__init__(**kwargs)
        self.view_model = view_model
        
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        self.title_label = MDLabel(
            text="Products",
            halign="center",
            size_hint_y=None,
            height=50
        )
        layout.add_widget(self.title_label)
        
        # Error message
        self.error_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Error",
            size_hint_y=None,
            height=30
        )
        layout.add_widget(self.error_label)
        
        # Products list
        scroll = ScrollView()
        self.products_list = MDList()
        scroll.add_widget(self.products_list)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
        
        # Load products
        self.view_model.load_products()
        self.update_products_list()
    
    def update_products_list(self):
        self.products_list.clear_widgets()
        if self.view_model.error_message:
            self.error_label.text = self.view_model.error_message
        else:
            self.error_label.text = ""
            for product in self.view_model.products:
                item = TwoLineListItem(
                    text=product.name,
                    secondary_text=f"Price: ${product.price:.2f}",
                    on_release=lambda x, p=product: self.show_product_details(p)
                )
                self.products_list.add_widget(item)
    
    def show_product_details(self, product):
        self.view_model.select_product(product.id)
        self.manager.current = 'product_details'

class ProductDetailsScreen(MDScreen):
    def __init__(self, view_model: ProductViewModel, **kwargs):
        super().__init__(**kwargs)
        self.view_model = view_model
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Back button
        self.back_button = MDRaisedButton(
            text="Back to List",
            pos_hint={'center_x': .5},
            on_release=self.go_back
        )
        layout.add_widget(self.back_button)
        
        # Product details card
        self.details_card = MDCard(
            orientation='vertical',
            padding=15,
            spacing=10,
            size_hint=(None, None),
            size=("300dp", "400dp"),
            pos_hint={"center_x": .5, "center_y": .5}
        )
        
        self.name_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Primary"
        )
        self.details_card.add_widget(self.name_label)
        
        self.price_label = MDLabel(
            text="",
            halign="center"
        )
        self.details_card.add_widget(self.price_label)
        
        self.description_label = MDLabel(
            text="",
            halign="center"
        )
        self.details_card.add_widget(self.description_label)
        
        self.quantity_label = MDLabel(
            text="",
            halign="center"
        )
        self.details_card.add_widget(self.quantity_label)
        
        layout.add_widget(self.details_card)
        self.add_widget(layout)
    
    def on_enter(self):
        if self.view_model.selected_product:
            product = self.view_model.selected_product
            self.name_label.text = product.name
            self.price_label.text = f"Price: ${product.price:.2f}"
            self.description_label.text = f"Description: {product.description}"
            self.quantity_label.text = f"Available: {product.quantity}"
    
    def go_back(self, *args):
        self.manager.current = 'product_list'

class CrossPlatformApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        
        # Initialize service and view model
        product_service = ProductService("http://your-backend-url/api")
        view_model = ProductViewModel(product_service)
        
        # Create screens
        product_list = ProductListScreen(view_model, name='product_list')
        product_details = ProductDetailsScreen(view_model, name='product_details')
        
        # Add screens to manager
        self.screen_manager = MDScreen()
        self.screen_manager.add_widget(product_list)
        self.screen_manager.add_widget(product_details)
        
        return self.screen_manager

if __name__ == '__main__':
    CrossPlatformApp().run() 