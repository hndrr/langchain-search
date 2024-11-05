type SourceMessageProps ={
    sources: string[];
}

export const SourceMessage: React.FC<SourceMessageProps> = ({sources}) => {
    return (
        <div className="py-2">
            <h2 className="text-gray-500">
                Sources
            </h2>
            <ol className="list-decimal text-sm pl-4">
                {sources.map((source, index) => (
                    <li key={"list" + index} className="text-gray-500">
                        {source}
                    </li>
                ))}
            </ol>
        </div>
    );
}

