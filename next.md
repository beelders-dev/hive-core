# Next Session

## Where I stopped
Working on reusable tabs for the ingredient/recipe detail pages.

## What I was doing
Creating a reusable HTMX tab button component.

## Next step
- Finish the tab component
- Test switching tabs with HTMX
- Make sure the URL/target are reusable

## Important thought
The tab button currently looks like:

<button hx-get="{{ url }}" hx-target="{{ target_div }}">
    {{ tab_name }}
</button>

## Don't forget
Keep the component generic rather than making it specific to one page.