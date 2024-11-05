type SearchMessageProps ={
    content: string;
}

export const SearchMessage: React.FC<SearchMessageProps> = ({content}) => {
    return (
        <div className="py-2">
                <p className="text-gray-500">
                    {content} で検索
                </p>
        </div>
    );
}

